import express from "express";
import axios from "axios";
import s3 from "../config/s3";
import db from "../database/db";
import { RowDataPacket } from "mysql2";
interface TestingData {
  sourceCode: string;
  testCases: { [key: string]: [] };
}
interface IQueryResult extends RowDataPacket {
  productName: string;
  courseName: string;
  lessonName: string;
  problemName: string;
}

interface Task {
  taskId: string;
  sourceCode: string;
  languageId: number;
  expectedOutput: string;
}

const allowedExtensions = [".json", ".py", ".js", ".java", ".c"]; // TODO: set globally

const findProblemInDB: (problemId: string) => Promise<IQueryResult[]> = (
  problemId
) => {
  return new Promise((resolve, reject) => {
    db.query(
      `SELECT Product.pathName as productName, Course.pathName as courseName, Lesson.pathName as lessonName, problemName, executeFile FROM PracticeProblem 
                  JOIN Lesson ON PracticeProblem.lessonId = Lesson.id
                  JOIN Course ON Lesson.courseId = Course.id
                  JOIN Product ON Course.productId = Product.id
              WHERE PracticeProblem.id = '${problemId}'`,
      (err: Error, result: IQueryResult[]) => {
        if (err) {
          reject(err);
        }
        resolve(result);
      }
    );
  });
};

const createTestingData = async (basePath: string, sourceCode: string) => {
  const params = {
    Bucket: process.env.TRAICODE_PRACTICE_PROBLEM_S3_BUCKET,
    Prefix: basePath,
  };

  const listObject = await s3.listObjectsV2(params).promise();
  // Extract file names from the 'Contents' property of the response
  const files = listObject.Contents.filter((object: any) =>
    allowedExtensions.includes(
      object.Key.substring(object.Key.lastIndexOf("."))
    )
  ).map((object: any) => object.Key);
  // console.log("Files in folder:", listObject.Contents);
  const promises = files.map(async (fileKey: any) => {
    // const fileKey = object.Key;
    const data = await s3
      .getObject({
        Bucket: process.env.TRAICODE_PRACTICE_PROBLEM_S3_BUCKET,
        Key: fileKey,
      })
      .promise();

    const fileContent = data.Body.toString();
    if (fileKey.includes("data.json")) {
      return { testCases: JSON.parse(fileContent) };
    } else if (fileKey.includes("template.py")) {
      const userCode: string = fileContent.replace("#{{CODE}}", sourceCode);
      return { sourceCode: userCode };
    } else {
      return;
    }
  });

  const result = await Promise.all(promises).then((obj) => {
    const data: TestingData = {
      sourceCode: "",
      testCases: {},
    };
    obj.forEach((item) => {
      if (item["sourceCode"]) {
        data.sourceCode = item["sourceCode"];
      }
      if (item["testCases"]) {
        data.testCases = item["testCases"];
      }
    });
    return data;
  });

  return result;
};

const createTasks = async (data: TestingData) => {
  const { sourceCode, testCases } = data;
  const result: Task[] = [];
  Object.keys(testCases).forEach((key: string) => {
    testCases[key].forEach((testCase: any, index: number) => {
      const taskId = key + "-" + index;
      result.push({
        taskId: taskId,
        sourceCode: sourceCode.replace("#{{TESTCASE}}", testCase["testCode"]),
        languageId: 71, // TODO: Replace w variable later
        expectedOutput: testCase["expected"] + "\n",
      });
    });
  });
  return result;
};

const executeTasks = async (tasks: Task[]) => {
  // Match tasks to batch submission format
  const batch = tasks.map((task) => {
    const { sourceCode, languageId, expectedOutput } = task;
    return {
      source_code: sourceCode,
      language_id: languageId,
      expected_output: expectedOutput,
    };
  });

  // Create batch submission
  const res = await axios
    .post(
      // TODO: Replace with the localhost URL when deployed
      // "http://localhost:2358/submissions?base64_encoded=true&wait=true",
      "http://54.185.233.196:2358/submissions/batch?base64_encoded=false",
      {
        submissions: batch,
      }
    )
    .then((response) => {
      console.log("Tasks", response.data);
      return response.data;
    })
    .catch((error) => {
      return error;
    });

  const tokens = await Promise.all(
    res.map(async (task: any) => {
      return task["token"];
    })
  );

  return tokens;
};
async function checkSubmissionStatus(tokens: string[]) {
  const url = `http://54.185.233.196:2358/submissions/batch?tokens=${tokens.join(
    ","
  )}&base64_encoded=false`;
  console.log("Checking submission status:", url);
  try {
    const response = await axios.get(url);
    const submissions = response.data.submissions;
    // Check if all submissions are completed
    const allCompleted = submissions.every(
      (submission: { status: { id: number } }) =>
        submission.status.id !== 1 && submission.status.id !== 2
    );

    if (!allCompleted) {
      // If not all submissions are completed, wait for some time and check again
      await new Promise((resolve) => setTimeout(resolve, 2000)); // Wait for 5 seconds
      return checkSubmissionStatus(tokens); // Recursively call the function to check status again
    } else {
      // All submissions are completed
      console.log("All submissions have completed.");
      return submissions;
    }
  } catch (error) {
    console.error("Error checking submission status:", error);
  }
}
// export const getSubmission = async (
//   req: express.Request,
//   res: express.Response
// ) => {
//   try {
//     const { token } = req.query;
//     if (!token) {
//       return res.status(400).json({ message: "Invalid submission token" });
//     }
//     // Get submission
//     const response = await axios.get(
//       `http://54.185.233.196:2358/submissions/${token}?base64_encoded=false`
//     );

//     if (!response.data) {
//       return res.status(500).json({ message: "Failed to get submission" });
//     }

//     // console.log("stdout data:", atob(response.data.stdout));
//     return res.status(200).json(response.data);
//   } catch (error: any) {
//     return res.status(500).json({ message: error.message });
//   }
// };

export const getSubmissions = async (
  req: express.Request,
  res: express.Response
) => {
  try {
    const { token } = req.query;
    if (!token) {
      return res.status(400).json({ message: "Invalid submission token" });
    }
    // Get submission
    const response = await axios.get(
      `http://54.185.233.196:2358/submissions/batch?tokens=${token}&base64_encoded=false`
    );

    if (!response.data) {
      return res.status(500).json({ message: "Failed to get submission" });
    }

    // console.log("stdout data:", atob(response.data.stdout));
    return res.status(200).json(response.data);
  } catch (error: any) {
    return res.status(500).json({ message: error.message });
  }
};

export const createSubmissions = async (
  req: express.Request,
  res: express.Response
) => {
  try {
    const { problemId, sourceCode, languageId } = req.body;
    // Validate input
    if (!problemId || !sourceCode || !languageId) {
      return res.status(400).json({ message: "Invalid input" });
    }
    // Find problem in DB
    const query = await findProblemInDB(problemId as string);
    const basePath = query.map((row: RowDataPacket) => {
      return [
        row.productName,
        row.courseName,
        row.lessonName,
        "practice-problems",
        "testing",
      ].join("/");
    })[0];

    const testingData = await createTestingData(basePath, sourceCode);

    // Create tasks from testing data
    const tasks = await createTasks(testingData);

    const tokens = await executeTasks(tasks);

    const submissons = await checkSubmissionStatus(tokens);

    const finalResult = [];
    for (let i = 0; i < submissons.length; i++) {
      const submission = submissons[i];
      const taskId = tasks[i].taskId;

      finalResult.push({
        taskId: taskId,
        submission: submission,
      });
    }

    // console.log("Final result:", finalResult);
    // if (executionTasks === undefined) {
    //   return res.status(500).json({ message: "Failed to create submission" });
    // }

    // const finalResult = await getResults(tasks, executionTasks);
    // console.log("Final result:", finalResult);
    // const encodedSourceCode = Buffer.from(result["sourceCode"]).toString(
    //   "base64"
    // );

    // const encodedResult = Buffer.from(result["output"]).toString("base64");

    // Submission created successfully
    // console.log("Submission created:", response.data);
    return res.status(200).json(finalResult);

    // return res.status(200).json({ message: "Submission created" });
  } catch (error: any) {
    return res.status(500).json({ message: error.message });
  }
};

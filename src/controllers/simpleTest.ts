import express from "express";
import axios from "axios";
import db from "../database/db";
import { RowDataPacket } from "mysql2";
import { storeSubmission } from "../services/submissions";
import { getAllFiles, readFileAsync } from "../utils";

interface Task {
  sourceCode: string;
  testCases: [];
}
interface PracticeQueryResult extends RowDataPacket {
  productName: string;
  courseName: string;
  lessonName: string;
  problemName: string;
}

const findPracticeProblemInDB: (
  problemId: string
) => Promise<PracticeQueryResult[]> = (problemId) => {
  return new Promise((resolve, reject) => {
    db.query(
      `SELECT Product.pathName as productName, Course.pathName as courseName, Lesson.pathName as lessonName, problemName, executeFile FROM PracticeProblem 
                  JOIN Lesson ON PracticeProblem.lessonId = Lesson.id
                  JOIN Course ON Lesson.courseId = Course.id
                  JOIN Product ON Course.productId = Product.id
              WHERE PracticeProblem.id = '${problemId}'`,
      (err: Error, result: PracticeQueryResult[]) => {
        if (err) {
          reject(err);
        }
        resolve(result);
      }
    );
  });
};

const prepareSubmission = async (directoryPath: string, sourceCode: string) => {
  const filesPath = getAllFiles(directoryPath);

  const promises = filesPath.map(async (file: any) => {
    const data = (await readFileAsync(file)) as string;

    const fileName = file.substring(file.lastIndexOf("/") + 1);

    if (fileName === "data_simple_test.json") {
      return { testCases: JSON.parse(data) };
    } else if (fileName === "template_simple_test.py") {
      const [_, toBeSubmitted] = sourceCode.split(
        "#------------------------***YOUR IMPLEMENTATION***------------------------#"
      );

      const userCode: string = data.replace("#{{CODE}}", toBeSubmitted);
      return { sourceCode: userCode };
    } else {
      return;
    }
  });

  const result = await Promise.all(promises).then((obj) => {
    const data: Task = {
      sourceCode: "",
      testCases: [],
    };
    obj.forEach((item) => {
      if (!item) return;
      const { sourceCode, testCases } = item;
      if (sourceCode !== undefined) {
        data.sourceCode = item["sourceCode"];
      } else if (testCases !== undefined) {
        data.testCases = item["testCases"];
      }
    });
    return data;
  });

  return result;
};

const executeTasks = async (task: Task) => {
  // Create batch submission
  const token = await axios
    .post(
      `${process.env.JUDGE0_DOCKER_URL}/submissions/?base64_encoded=false`,
      {
        source_code: task["sourceCode"],
        language_id: 71, // TODO: Replace w variable later
      }
    )
    .then((response) => {
      return response.data.token;
    })
    .catch((error) => {
      return error;
    });

  return token;
};
async function checkSubmissionStatus(token: string) {
  const url = `${process.env.JUDGE0_DOCKER_URL}/submissions/${token}?base64_encoded=false`;
  console.log("Checking submission status:", url);
  try {
    const response = await axios.get(url);
    const submission = response.data;
    // Check if all submissions are completed
    const isCompleted =
      submission.status.id !== 1 && submission.status.id !== 2;

    if (!isCompleted) {
      // If not all submissions are completed, wait for some time and check again
      await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait for 1 second
      return checkSubmissionStatus(token); // Recursively call the function to check status again
    } else {
      // All submissions are completed
      console.log("All submissions have completed.");
      return submission;
    }
  } catch (error) {
    console.error("Error checking submission status:", error);
  }
}

export const createSimpleTest = async (
  req: express.Request,
  res: express.Response
) => {
  try {
    const { userId, problemId, sourceCode, languageId } = req.body;
    // Validate input
    if (!userId || !problemId || !sourceCode || !languageId) {
      return res.status(400).json({ message: "Invalid input" });
    }
    // Find problem in DB
    const query = await findPracticeProblemInDB(problemId as string);
    const basePath = query.map((row: RowDataPacket) => {
      return [
        "traicode-coursework-bucket",
        row.productName,
        row.courseName,
        row.lessonName,
        "practice-problems",
        "test-cases",
      ].join("/");
    })[0];

    const directoryPath =
      process.env.BASE_URL_EC2_PATH ||
      process.env.BASE_URL_LOCAL_PATH + basePath;

    const task = await prepareSubmission(directoryPath, sourceCode);

    const token = await executeTasks(task);
    // console.log("Token:", token);
    const submisson = await checkSubmissionStatus(token);
    console.log("Simple Test Submission:", submisson);

    const statusIndicator = submisson["stdout"].split("\n")[0];
    let status;
    if (statusIndicator.includes("E")) {
      status = "Compile Error";
    } else if (statusIndicator.includes("F")) {
      status = "Wrong Answer";
    } else {
      status = "Accepted";
    }

    const [output, reportResult] = submisson["stdout"].split(
      "****TEST_REPORT****"
    );

    // console.log("Report result:", reportResult);
    const result = {
      // sourceCode: task["sourceCode"],
      result: JSON.parse(reportResult),
      output: output,
      timeExecuted: submisson["time"],
      memoryUsed: submisson["memory"],
      token: submisson["token"],
      status: status,
    };
    return res.status(200).json(result);

    // return res.status(200).json({ message: "Submission created" });
  } catch (error: any) {
    return res.status(500).json({ message: error.message });
  }
};

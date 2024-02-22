import express from "express";
import db from "../database/db";
import { RowDataPacket } from "mysql2";
import { detectLanguage, getAllFiles, readFileAsync } from "../utils";

interface PracticeProblem {
  content: string;
  sourceCode: {
    fileName: string;
    language: string;
    executeFile: boolean;
    code: string;
  }[];
  solution: {
    fileName: string;
    language: string;
    code: string;
  }[];
  testCaseSimple: {
    testName: string;
    input: string;
    output: string;
  }[];
  testCaseFull: {
    testName: string;
    input: string;
    output: string;
  }[];
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

export const getPracticeProblems = async (
  req: express.Request,
  res: express.Response
) => {
  try {
    const { problemId } = req.query;
    if (!problemId) {
      return res.status(400).json({ message: "Invalid practice problem id" });
    }
    const queryResult = await findPracticeProblemInDB(problemId as string);
    const basePath = queryResult.map((row: RowDataPacket) => {
      return [
        "traicode-coursework-bucket",
        row.productName,
        row.courseName,
        row.lessonName,
        "practice-problems",
      ].join("/");
    })[0];

    const directoryPath =
      process.env.BASE_URL_EC2_PATH ||
      process.env.BASE_URL_LOCAL_PATH + basePath;
    const filesPath = getAllFiles(directoryPath);

    const promises = filesPath.map(async (file: string) => {
      const data = (await readFileAsync(file)) as string;

      const fileName = file.substring(file.lastIndexOf("/") + 1);
      const isExecuteFile = fileName === queryResult[0].executeFile;

      if (file.includes("/content/") && fileName === "index.md") {
        return { content: data };
      } else if (file.includes("/source-code/")) {
        return {
          sourceCode: {
            fileName: fileName,
            language: detectLanguage(fileName),
            executeFile: isExecuteFile,
            code: data,
          },
        };
      } else if (file.includes("/solution/")) {
        return {
          solution: {
            fileName: fileName,
            language: detectLanguage(fileName),
            code: data,
          },
        };
      } else if (
        file.includes("/test-cases/") &&
        fileName === "data_simple_test.json"
      ) {
        return { testCaseSimple: JSON.parse(data) };
      } else if (
        file.includes("/test-cases/") &&
        fileName === "data_full_test.json"
      ) {
        return { testCaseFull: JSON.parse(data) };
      }
    });

    const results = await Promise.all(promises).then((obj) => {
      //   console.log("obj", obj);
      const practiceProblem: PracticeProblem = {
        content: "",
        sourceCode: [],
        solution: [],
        testCaseSimple: [],
        testCaseFull: [],
      };
      obj.forEach((value) => {
        if (!value) return;

        const { content, sourceCode, solution, testCaseSimple, testCaseFull } =
          value;

        if (content !== undefined) {
          practiceProblem.content = content;
        } else if (sourceCode !== undefined) {
          practiceProblem.sourceCode.push(sourceCode);
        } else if (solution !== undefined) {
          practiceProblem.solution.push(solution);
        } else if (testCaseSimple !== undefined) {
          practiceProblem.testCaseSimple = testCaseSimple;
        } else if (testCaseFull !== undefined) {
          practiceProblem.testCaseFull = testCaseFull;
        }
      });

      return practiceProblem;
    });
    return res.status(200).json(results);
    // return res.status(200).json({ message: "Success" });
  } catch (error: any) {
    return res.status(500).json({ message: error.message });
  }
};

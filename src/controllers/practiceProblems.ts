import express from "express";
import s3 from "../config/s3";
import db from "../database/db";
import { RowDataPacket } from "mysql2";
import { detectLanguage } from "../utils";

interface PracticeProblem {
  content?: string;
  sourceCode?: {
    fileName: string;
    language: string;
    excuteFile: string;
    code: string;
  }[];
  solution?: {
    fileName: string;
    language: string;
    code: string;
  }[];
  testCases?: {
    testName: {
      input: string;
      output: string;
    }[];
  };
}

interface PracticeQueryResult extends RowDataPacket {
  productName: string;
  courseName: string;
  lessonName: string;
  problemName: string;
}
const allowedExtensions = [".md", ".py", ".js", ".java", ".c"]; // TODO: set globally

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

const getObjectFromS3 = async (bucket: string, key: string) => {
  const data = await s3.getObject({ Bucket: bucket, Key: key }).promise();
  return data.Body.toString();
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
        row.productName,
        row.courseName,
        row.lessonName,
        "practice-problems",
      ].join("/");
    })[0];

    const params = {
      Bucket: process.env.TRAICODE_PRACTICE_PROBLEM_S3_BUCKET,
      Prefix: basePath,
    };

    const listObject = await s3.listObjectsV2(params).promise();

    // Filter out directories
    const fileKeys = listObject.Contents.map(
      (object: any) => object.Key
    ).filter((key: string) => !key.endsWith("/"));

    const promises = fileKeys.map(async (fileKey: string) => {
      const fileContent = await getObjectFromS3(
        process.env.TRAICODE_PRACTICE_PROBLEM_S3_BUCKET as string,
        fileKey
      );
      const fileName = fileKey.substring(fileKey.lastIndexOf("/") + 1);
      const isExecuteFile = fileName === queryResult[0].executeFile;

      if (fileName === "index.md") {
        return { content: fileContent };
      } else if (fileKey.includes("/source-code/")) {
        return {
          sourceCode: {
            fileName: fileName,
            language: detectLanguage(fileName),
            executeFile: isExecuteFile,
            code: fileContent,
          },
        };
      } else if (fileKey.includes("/solution/")) {
        return {
          solution: {
            fileName: fileName,
            language: detectLanguage(fileName),
            executeFile: isExecuteFile,
            code: fileContent,
          },
        };
      } else if (fileKey.includes("/test-cases/") && fileName === "data.json") {
        return { testCases: JSON.parse(fileContent) };
      }
    });

    const results = await Promise.all(promises).then((obj) => {
      //   console.log("obj", obj);
      const practiceProblem: PracticeProblem = {
        content: "",
        sourceCode: [],
        solution: [],
        testCases: {
          testName: [],
        },
      };
      obj.forEach((value) => {
        if (!value) return;
        if (value.hasOwnProperty("content")) {
          practiceProblem.content = value.content;
        } else if (value.hasOwnProperty("sourceCode")) {
          practiceProblem?.sourceCode?.push(value["sourceCode"]);
        } else if (value.hasOwnProperty("solution")) {
          practiceProblem?.solution?.push(value["solution"]);
        } else if (value.hasOwnProperty("testCases")) {
          practiceProblem.testCases = value["testCases"];
        }
      });
      // const res = practiceProblem.sourceCode?.reduce((acc: any, cur: any) => {
      //   acc[cur.fileName] = cur;
      //   return acc;
      // }, []);
      return practiceProblem;
    });

    return res.status(200).json(results);
  } catch (error: any) {
    return res.status(500).json({ message: error.message });
  }
};

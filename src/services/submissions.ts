import db from "../database/db";
import { v4 as uuidv4 } from "uuid";

interface Submission {
  userId: string;
  problemId: string;
  tokenId: string;
  sourceCode: string;
  language: string;
  status: string;
  timeExecuted: string;
  memoryUsed: number;
}

const queryAsync = (sql: string, params: (string | number)[]) => {
  return new Promise((resolve, reject) => {
    db.query(sql, params, (err: Error, result: any) => {
      if (err) {
        reject(err);
      } else {
        resolve(result);
      }
    });
  });
};

export const storeSubmission = async (submission: Submission) => {
  try {
    const {
      userId,
      problemId,
      tokenId,
      sourceCode,
      language,
      status,
      timeExecuted,
      memoryUsed,
    } = submission;

    const submissionQuery =
      "INSERT INTO Submission (id, sourceCode, language, status, timeExecuted, memoryUsed) VALUES (?, ?, ?, ?, ?, ?)";
    const submissionValues = [
      tokenId,
      sourceCode,
      language,
      status,
      timeExecuted,
      memoryUsed,
    ];

    queryAsync(submissionQuery, submissionValues).then((result: any) => {
      if (result.affectedRows === 1) {
        console.log("Submission has been stored in the database.");
        const userSubmissionQuery =
          "INSERT INTO UserPracticeProblemProgress (id, userId, problemId, tokenId) VALUES (?, ?, ?, ?)";
        const userSubmissionValues = [uuidv4(), userId, problemId, tokenId];
        queryAsync(userSubmissionQuery, userSubmissionValues).then(
          (result: any) => {
            if (result.affectedRows === 1) {
              console.log("User submission has been stored in the database.");
            }
          }
        );
      }
    });
    // new Promise((resolve, reject) => {
    //   db.query(submissionQuery, submissionValues, (err: Error, result: any) => {
    //     if (err) {
    //       reject(err);
    //     }
    //     resolve(result);
    //   });
    // }).then((result: any) => {
    //   if (result.affectedRows === 1) {
    //     console.log("Submission has been stored in the database.");
    //     const userSubmissionQuery =
    //       "INSERT INTO UserSubmission (userId, submissionId, problemId) VALUES (?, ?, ?)";
    //     const userSubmissionValues = [userId, tokenId, problemId];
    //     db.query(
    //       userSubmissionQuery,
    //       userSubmissionValues,
    //       (err: Error, result: any) => {
    //         if (err) {
    //           console.error("Error storing user submission:", err);
    //         }

    //         if (result.affectedRows === 1) {
    //           console.log("User submission has been stored in the database.");
    //         }
    //       }
    //     );
    //   }
    // });
  } catch (error) {
    console.error("Error storing submission:", error);
  }
};

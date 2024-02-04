import express from "express";
import axios from "axios";

export const createSubmission = async (
  req: express.Request,
  res: express.Response
) => {
  try {
    const { problemId, sourceCode, languageId } = req.body;
    // Validate input
    if (!problemId || !sourceCode || !languageId) {
      return res.status(400).json({ message: "Invalid input" });
    }

    // Create submission
    const response = await axios.post(
      // TODO: Replace with the localhost URL when deployed
      "http://54.185.233.196:2358/submissions?base64_encoded=false&wait=true",
      {
        source_code: sourceCode,
        language_id: languageId,
      }
    );
    if (!response.data) {
      return res.status(500).json({ message: "Failed to create submission" });
    }
    // Submission created successfully
    return res.status(200).json(response.data);

    // return res.status(200).json({ message: "Submission created" });
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

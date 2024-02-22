import { createSimpleTest } from "./../controllers/simpleTest";
import express from "express";

export default (router: express.Router) => {
  // router.get("/submissions/batch", getSubmissions);
  router.post("/simpleTest", createSimpleTest);
};

const express = require("express");
const router = express.Router();
const controller = require("../controllers/file_controller");

let routes = (app) => {
  router.post("/files", controller.upload);
  router.get("/files", controller.getListFiles);
  router.get("/files/:name", controller.download);
  router.delete("/files/:name", controller.remove);

  app.use(router);
};

module.exports = routes;
if (process.env.NODE_ENV === 'development') {
  require('dotenv').config(); // Load .env file only in development
}

import express from 'express';
import multer from 'multer';

import { PORT as _PORT } from './config';
import { info } from './winston';

const app = express();
const PORT = _PORT


app.listen(PORT, () => {
  info(`Server is running on PORT : ${PORT}...`);
});

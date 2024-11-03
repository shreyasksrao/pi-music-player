const fs = require('fs')
const path = require('path')

const winston = require('winston');
const config = require('./config')

const APP_NAME = config.APP_NAME;
const LOG_DIR = config.LOG_DIR;
const LOG_LEVEL = config.LOG_LEVEL

const MAX_LOG_FILE_SIZE = 5 * 1024 * 1024;

// Creates log directory if it doesn't exist
if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR);
}
const logFilePath = path.join(LOG_DIR, `${APP_NAME}.log`);

const rotateLogFile = () => {
    const stats = fs.statSync(logFilePath);
    if (stats.size > MAX_LOG_FILE_SIZE) {
        const timestamp = new Date().toISOString().replace(/:/g, '-').split('.')[0]; // Create a timestamp
        const newLogFilePath = path.join(LOG_DIR, `${APP_NAME}-${timestamp}.log`);
        fs.renameSync(logFilePath, newLogFilePath); // Rename the log file
        fs.writeFileSync(logFilePath, ''); // Create a new log file
    }
};

const logger = winston.createLogger({
  level: LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(), 
    winston.format.printf(({ timestamp, level, message }) => {
        const module = process.title; // Use the process title as the module name
        return `${timestamp} ${level.toUpperCase()} ${module} ${message}`; // Format the log message
    })
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: logFilePath }) 
  ],
});

// Override the logger's log method to check for rotation
const originalLog = logger.log.bind(logger);
logger.log = (level, message, ...meta) => {
    rotateLogFile(); // Check for log rotation before logging
    originalLog(level, message, ...meta); // Call the original log method
};

module.exports = logger;

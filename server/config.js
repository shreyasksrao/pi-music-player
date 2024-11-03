module.exports = {
    APP_NAME:      process.env.APP_NAME || 'file-uploader',
    LOG_LEVEL:     process.env.LOG_LEVEL || 'info',
    LOG_DIR:       process.env.LOG_DIR,
    PORT :         process.env.SERVER_PORT || 9000,
    UPLOAD_DIR :   process.UPLOAD_DIR,
}

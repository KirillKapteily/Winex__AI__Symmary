import { exec } from "child_process";

import open from "open";


// Запуск Flask-сервера
const flaskProcess = exec("python app.py", (error, stdout, stderr) => {
    if (error) {
        console.error(`Ошибка запуска Flask-сервера: ${error.message}`);
        return;
    }
    if (stderr) {
        console.error(`Flask сервер stderr: ${stderr}`);
        return;
    }
    console.log(`Flask сервер stdout: ${stdout}`);
});

// Даем серверу время на запуск (2 секунды), затем открываем браузер
setTimeout(() => {
    open("http://127.0.0.1:5000");
}, 2000);

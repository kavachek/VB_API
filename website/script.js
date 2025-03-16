document.getElementById("generateOrdersBtn").addEventListener("click", function() {
    // Получаем значения из полей для даты (формат ГГГГ-ММ-ДД)
    const startDateStr = document.getElementById("startDate").value;
    const endDateStr = document.getElementById("endDate").value;

    // Преобразуем строку в объект Date
    const startDateParts = startDateStr.split("-");
    const endDateParts = endDateStr.split("-");

    const startDate = new Date(startDateParts[0], startDateParts[1] - 1, startDateParts[2]); // Месяцы от 0 до 11
    const endDate = new Date(endDateParts[0], endDateParts[1] - 1, endDateParts[2]);

    console.log("Начальная дата:", startDate);
    console.log("Конечная дата:", endDate);
});

document.getElementById("generateStocksBtn").addEventListener("click", function() {
    console.log("Генерация отчета по остаткам...");
});

document.getElementById("generateAllBtn").addEventListener("click", function() {
    console.log("Генерация общего отчета...");
});

document.getElementById("savePathBtn").addEventListener("click", function() {
    const savePath = document.getElementById("savePath").value;
    console.log("Путь для сохранения:", savePath);
});

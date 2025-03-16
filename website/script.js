document.addEventListener("DOMContentLoaded", function () {
    const onlineBtn = document.getElementById("onlineBtn");
    const reportBtn = document.getElementById("reportBtn");
    const reportSection = document.getElementById("reportSection");
    const onlineSection = document.getElementById("onlineSection");

    onlineBtn.addEventListener("click", function () {
        onlineSection.style.display = "block";
        reportSection.style.display = "none";
    });

    reportBtn.addEventListener("click", function () {
        reportSection.style.display = "block";
        onlineSection.style.display = "none";
    });

    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    function generateReport(type) {
        const startDateStr = document.getElementById("startDate").value;
        const endDateStr = document.getElementById("endDate").value;
        const savePath = document.getElementById("savePath").value;

        if (!startDateStr || !endDateStr) {
            alert("Пожалуйста, выберите начальную и конечную дату.");
            return;
        }

        if (!savePath) {
            alert("Укажите путь для сохранения отчета.");
            return;
        }

        const startDate = new Date(startDateStr);
        const endDate = new Date(endDateStr);

        const formattedStartDate = formatDate(startDate);
        const formattedEndDate = formatDate(endDate);

        console.log(`Генерация отчета: ${type}`);
        console.log("Начальная дата:", formattedStartDate);
        console.log("Конечная дата:", formattedEndDate);
        console.log("Путь для сохранения:", savePath);
    }

    document.getElementById("generateOrdersBtn").addEventListener("click", function () {
        generateReport("Заказы");
    });

    document.getElementById("generateStocksBtn").addEventListener("click", function () {
        generateReport("Остатки");
    });

    document.getElementById("generateAllBtn").addEventListener("click", function () {
        generateReport("Общий отчет");
    });

    document.getElementById("savePathBtn").addEventListener("click", function () {
        const savePath = document.getElementById("savePath").value;

        if (!savePath) {
            alert("Введите путь для сохранения файлов.");
            return;
        }

        fetch('http://127.0.0.1:5000/save_path', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ path: savePath }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            alert("Ошибка при отправке запроса на сервер.");
        });
    });

    const startDateInput = document.getElementById("startDate");
    const endDateInput = document.getElementById("endDate");

    startDateInput.addEventListener("input", function () {
        const value = this.value;
        if (value.length > 10) {
            this.value = value.slice(0, 10);
        }
    });

    endDateInput.addEventListener("input", function () {
        const value = this.value;
        if (value.length > 10) {
            this.value = value.slice(0, 10);
        }
    });
});
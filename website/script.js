document.addEventListener("DOMContentLoaded", function () {
    const onlineBtn = document.getElementById("onlineBtn");
    const reportBtn = document.getElementById("reportBtn");

    const reportSection = document.getElementById("reportSection");
    const onlineSection = document.getElementById("onlineSection");

    const savePathInput = document.getElementById("savePath");

    fetch("http://127.0.0.1:5000/get_saved_path", {
        method: "GET",
    })
    .then(response => response.json())
    .then(data => {
        if (data.path) {
            savePathInput.value = data.path;
        }
    })
    .catch(error => {
        console.error("Ошибка при получении пути:", error);
    });

    onlineBtn.addEventListener("click", function () {
        onlineSection.style.display = "block";
        reportSection.style.display = "none";
    });

    reportBtn.addEventListener("click", function () {
        reportSection.style.display = "block";
        onlineSection.style.display = "none";
    });

    function convertDateFormat(dateStr) {
        const parts = dateStr.split(".");
        if (parts.length === 3) {
            return `${parts[2]}-${parts[1]}-${parts[0]}`;
        }
        return null;
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

        const formattedStartDate = convertDateFormat(startDateStr);
        const formattedEndDate = convertDateFormat(endDateStr);

        if (!formattedStartDate || !formattedEndDate) {
            alert("Ошибка в формате даты. Используйте ДД.ММ.ГГГГ.");
            return;
        }

        fetch("http://127.0.0.1:5000/generate_report", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                start_date: formattedStartDate,
                end_date: formattedEndDate,
                report_type: type
            }),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || "Ошибка на сервере");
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(`Ошибка: ${data.error}`);
            } else {
                alert(data.message || "Отчет создан.");
            }
        })
        .catch(error => {
            alert(`Ошибка: ${error.message}`);
        });
    }

    document.getElementById("generateOrdersBtn").addEventListener("click", function () {
        generateReport("sales");
    });

    document.getElementById("generateStocksBtn").addEventListener("click", function () {
        generateReport("stocks");
    });

    document.getElementById("generateAllBtn").addEventListener("click", function () {
        generateReport("both");
    });

    document.getElementById("savePathBtn").addEventListener("click", function () {
        const savePath = document.getElementById("savePath").value;

        if (!savePath) {
            alert("Введите путь для сохранения файлов.");
            return;
        }

        fetch("http://127.0.0.1:5000/save_path", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ path: savePath }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message || "Путь сохранен успешно.");
            }
        })
        .catch(error => {
            alert("Ошибка при отправке запроса на сервер.");
        });
    });

    function applyDateMask(inputElement) {
        inputElement.addEventListener("input", function (event) {
            let value = this.value.replace(/\D/g, "");
            if (value.length > 8) value = value.slice(0, 8);

            if (value.length >= 2) value = value.slice(0, 2) + "." + value.slice(2);
            if (value.length >= 5) value = value.slice(0, 5) + "." + value.slice(5);

            this.value = value;
        });

        inputElement.addEventListener("blur", function () {
            if (!/^\d{2}\.\d{2}\.\d{4}$/.test(this.value)) {
                alert("Введите дату в формате ДД.ММ.ГГГГ.");
                this.value = "";
            }
        });
    }

    applyDateMask(document.getElementById("startDate"));
    applyDateMask(document.getElementById("endDate"));

    document.getElementById("integrateGoogleSheetsBtn").addEventListener("click", function () {
        window.location.href = "https://docs.google.com/spreadsheets/d/1GY62zEbBdg1MuR55gtPQvQkHsxu2Z3vGs9E7MxAhS5A";
    });
});
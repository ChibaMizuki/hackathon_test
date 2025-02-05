document.addEventListener("DOMContentLoaded", function () {
    let warned = false; // すでに警告を出したかを追跡するフラグ
    const fullDayOff = document.getElementById("id_full_day_off"); // フォームの全休
    const excludedPeriods = document.querySelectorAll("input[name='excluded_periods']"); // 入れない時限

    function checkWarning() {
        const fullDayOffValue = parseInt(fullDayOff.value, 10);
        const allChecked = Array.from(excludedPeriods).every(input => input.checked);

        if (!warned && (fullDayOffValue === 5 || allChecked)) {
            alert("理系なめてる？");
            warned = true;
        }
    }

    if (fullDayOff) {
        fullDayOff.addEventListener("change", checkWarning);
    }

    if (excludedPeriods.length > 0) {
        excludedPeriods.forEach(input => input.addEventListener("change", checkWarning));
    }
});

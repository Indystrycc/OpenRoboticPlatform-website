window.addEventListener("DOMContentLoaded", () => {
    for (const timeEl of document.querySelectorAll("time")) {
        try {
            const date = new Date(timeEl.dateTime);
            if (date.valueOf() === NaN) throw new Error("Invalid date: " + timeEl.dateTime);
            timeEl.textContent = date.toLocaleString();
        } catch (error) {
            console.warn("Failed to parse date", error);
        }
    }
});

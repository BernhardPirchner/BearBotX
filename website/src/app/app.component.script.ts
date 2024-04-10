function openPopup(id: string): void {
    const popup = document.getElementById(id);
    if (popup) {
        popup.style.display = "flex";
    }
}

function closePopup(id: string): void {
    const popup = document.getElementById(id);
    if (popup) {
        popup.style.display = "none";
    }
}



window.addEventListener("DOMContentLoaded", () => {
    const categoryModal = document.getElementById("categoryEditModal");
    if (!categoryModal) return;

    categoryModal.addEventListener("show.bs.modal", e => {
        const button = e.relatedTarget;
        const categoryId = button.getAttribute("data-category-id") ?? "-1";

        const modalTitle = document.getElementById("categoryEditLabel");
        const nameInput = document.getElementById("categoryName");
        const parentCategorySelect = document.getElementById("parentCategory");
        const saveButton = categoryModal.querySelector("button.btn-primary[type=submit]");
        const categoryIdInput = document.getElementById("categoryId");

        categoryIdInput.value = categoryId;
        if (categoryId == "-1") {
            modalTitle.textContent = "New category";
            nameInput.value = "";
            parentCategorySelect.value = "-1";
            saveButton.textContent = "Create category";
        } else {
            const categoryName = button.getAttribute("data-category-name") ?? "";
            const parentId = button.getAttribute("data-parent-id") ?? "-1";

            modalTitle.textContent = `Edit category ${categoryName}`;
            nameInput.value = categoryName;
            parentCategorySelect.value = parentId;
            saveButton.textContent = "Save";
        }
    });
});

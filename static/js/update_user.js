document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("#update-form");
    const container = document.querySelector("#update-container");
    const updateUrl = container.dataset.urlUpdate;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = Object.fromEntries(new FormData(e.target).entries());

        const res = await fetch(updateUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const json = await res.json();
        alert(json.message || json.error);
        if (json.redirect) window.location.href = json.redirect;
    });
});
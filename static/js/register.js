document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("#register-form");
    const container = document.querySelector("#register-container");
    const registerUrl = container.dataset.urlRegister;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = Object.fromEntries(new FormData(e.target).entries());

        try {
            const res = await fetch(registerUrl, {
                method: "POST",
                headers: {"Content-Type" : "Application/json"},
                body: JSON.stringify(data),
            });

            const text = await res.text();
            let result;

            try {
                result = JSON.parse(text);
            } catch {
                console.log("Resposta não é JSON", text);
                alert("Erro inesperado no servidor.");
                return;
            }

            if (res.ok){
                alert("Usuário registrado com sucesso!");
                window.location.href = "/login/";
            }
            else {
                alert(result.error || "Erro ao registrar usuário.");
            }
        } catch (error) {
            console.error(error);
            alert("Ocorreu um erro ao registrar. Tente novamente");
        }
    });
});
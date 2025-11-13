document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("#login-form");
    const container = document.querySelector("#login-container");
    const loginUrl = container.dataset.urlLogin;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(e.target).entries());


        try {
            const res = await fetch(loginUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });

            const text = await res.text();
            let result;
            try {
                result = JSON.parse(text);
            } catch {
                console.log("Resposta não é JSON:", text);
                alert("Erro inesperado no servidor");
                return;
            }

            if (res.ok) {
                alert("Login realizado com sucesso!");
                // ✅ Redireciona para o calendário
                window.location.href = "/";
            } else {
                alert(result.error || "Erro ao fazer login");
            }
        } catch (err) {
            console.error(err);
            alert("Erro ao se conectar com o servidor");
        }
    });

});
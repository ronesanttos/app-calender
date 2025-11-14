// ✅ Função segura para capturar CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

document.addEventListener("DOMContentLoaded", function () {
  const calendarEl = document.getElementById("calendar");

  // ✅ Agora funciona, porque vem do HTML
  const eventosURL = calendarEl.dataset.urlEventos;

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    locale: "pt-br",
    height:"auto",
    contentHeight: "auto",
    expandRows: true,
    selectable: true,
    headerToolbar: {
      left: "prev,next today",
      center: "title",
      right: "dayGridMonth,timeGridWeek,listMonth",
    },
    buttonText: {
      today: "Hoje",
      month: "Mês",
      week: "Semana",
      list: "Agenda",
    },

    // ✅ Correto agora
    events: eventosURL,

    dateClick: function (info) {
      const nome = prompt(`Para quem você trabalhou hoje [${info.dateStr}]:`);

      if (nome) {
        fetch(eventosURL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({
            nome: nome,
            data_evento: info.dateStr,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.error) {
              alert("Erro: " + data.error);
            } else {
              calendar.addEvent(data);
            }
          })
          .catch((err) => console.log("Erro ao salvar evento:", err));
      }
    },

    eventClick: function (info) {
      const acao = prompt(
        `Evento: ${info.event.title}\n\n[1] Editar\n[2] Deletar`
      );

      if (acao === "1") {
        const novoNome = prompt("Novo nome:", info.event.title);

        if (novoNome && novoNome !== info.event.title) {
          fetch(eventosURL, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({
              id: info.event.id,
              nome: novoNome,
            }),
          })
            .then((r) => r.json())
            .then((data) => {
              if (!data.error) {
                info.event.setProp("title", data.title);
              } else {
                alert("Erro: " + data.error);
              }
            });
        }
      }

      if (acao === "2") {
        if (confirm(`Deseja excluir o evento "${info.event.title}"?`)) {
          fetch(eventosURL, {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({ id: info.event.id }),
          })
            .then((r) => r.json())
            .then((data) => {
              if (data.success) {
                info.event.remove();
              } else {
                alert("Erro ao excluir");
              }
            });
        }
      }
    },
  });

  calendar.render();
});

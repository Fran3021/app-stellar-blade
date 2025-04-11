document.addEventListener("DOMContentLoaded", function () {


  //script donde se configura el fondo animado a traves de la libreria tsparticles
  particlesJS("particles-js", {
    particles: {
      number: { value: 50 },
      color: { value: "#00BFFF" },
      shape: { type: "circle" },
      opacity: { value: 0.8, random: true },
      size: { value: 3, random: true },
      move: { enable: true, speed: 1, direction: "none", random: true },
    },
    interactivity: {
      detect_on: "canvas",
      events: { onhover: { enable: false } },
    },
    retina_detect: true,
  });


  //evento para seguir y dejar de seguir a usuarios
  const buttonsFollows = document.querySelectorAll(".ButtonFollows");
  let mensajeFollow = document.querySelector(".mensaje-follow");
  if (buttonsFollows) {
    buttonsFollows.forEach((buttonFollow) => {
      const perfilPk = buttonFollow.dataset.perfilId;
      let nSeguidores = document.getElementById(`Nseguidores-${perfilPk}`);
      buttonFollow.addEventListener("click", (event) => {
        event.preventDefault();
        fetch(buttonFollow.href)
          .then((response) => response.json())
          .then((data) => {
            nSeguidores.innerHTML = `<h3>Seguidores: ${data.numero_seguidores} </h3>`;
            if (data.follow) {
              buttonFollow.innerHTML =
                '<button type="button" class="btn btn-outline-primary btn-sm">Dejar de seguir</button>';
              mensajeFollow.innerHTML = `<p class="alert alert-primary">${data.mensaje}</p>`;
            } else {
              buttonFollow.innerHTML =
                ' <button type="button" class="btn btn-outline-dark btn-sm">Seguir</button>';
              mensajeFollow.innerHTML = `<p class="alert alert-danger">${data.mensaje}</p>`;
            }
          });
      });
    });
  }


  //evento para dar me gusta a una publicacion
  const LikesButtons = document.querySelectorAll(".LikesButtons");
  let mensajeLikes = document.querySelector(".mensaje-likes");
  if (LikesButtons) {
    LikesButtons.forEach((buttonLike) => {
      const publicacionPk = buttonLike.dataset.publicacionId;
      let nLikes = document.getElementById(`NumeroLikes-${publicacionPk}`);
      buttonLike.addEventListener("click", (event) => {
        event.preventDefault();
        fetch(buttonLike.href)
          .then((response) => response.json())
          .then((data) => {
            nLikes.innerHTML = data.numero_likes;
            if (data.like) {
              buttonLike.innerHTML = '<i class="bi bi-heart-fill"></i>';
              mensajeLikes.innerHTML = `<p class="alert alert-primary">${data.mensaje}</p>`;
            } else {
              buttonLike.innerHTML = '<i class="bi bi-heart"></i>';
              mensajeLikes.innerHTML = `<p class="alert alert-danger">${data.mensaje}</p>`;
            }
          });
      });
    });
  }


  //evento para poder responder a un comentario por peticion ajax
  const FormResponder = document.querySelectorAll(".FormRespuesta");
  let mensajesContestarComentarios = document.querySelector(
    ".mensajes-contestar-comentarios"
  );
  FormResponder.forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      let redirectUrl = form.getAttribute("data-redirect-url");

      const formData = new FormData(form); //aqui metemos todos los datos del formulario

      fetch(form.action, {
        //con esto evitamos que nos abra un json en otra pagina del navegador
        method: "POST",
        body: formData,
        header: {
          "X-Request-Width": "XMLHttpRequest", //le decimos a django que es una peticion Ajax
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.mensaje) {
            mensajesContestarComentarios.innerHTML = `<p class="alert alert-primary">${data.mensaje}</p>`;
            form.reset(); //con esto limpiamos el formulario

            setTimeout(() => {
              window.location.href = redirectUrl;
            }, 1000);
            
          } else {
            mensajesContestarComentarios.innerHTML = `<p class="alert alert-primary">${data.error}</p>`;
          }
        });
    });
  });


  //evento para abrir formulario para nuevo comentario
  let ButtonNuevoComentario = document.querySelectorAll(
    ".ButtonNuevoComentario"
  );
  let FormComentario = document.querySelector(".FormComentario");
  ButtonNuevoComentario.forEach((button) => {
    button.addEventListener("click", () => {
      FormComentario.classList.toggle("block");
    });
  });

  //evento para abrir formulario para responder comentarios
  let buttonResponderComentarios = document.querySelectorAll(".BotonResponder");
  buttonResponderComentarios.forEach((button) => {
    const comentarioPk = button.dataset.comentarioPk;
    const formRespuesta = document.getElementById(
      `FormRespuesta-${comentarioPk}`
    );
    button.addEventListener("click", () => {
      formRespuesta.classList.toggle("block");
    });
  });


  //evento para ver todos las respuestas de un comentario
  let buttonVerRespuestas = document.querySelectorAll(".VerRespuestas");
  buttonVerRespuestas.forEach((button) => {
    const comentarioPk = button.dataset.comentarioPk;
    const containerRespuestas = document.getElementById(
      `container-respuestas-${comentarioPk}`
    );
    button.addEventListener("click", () => {
      containerRespuestas.classList.toggle("block");
    });
  });


  //evento para eliminar comentario
  let buttonEliminarComentario = document.querySelectorAll(
    ".EliminarComentario"
  );
  let mensajesEliminarComentarios = document.querySelector(
    ".mensajes-eliminar-comentarios"
  );
  buttonEliminarComentario.forEach((button) => {
    let pkComentario = button.dataset.comentarioPk;
    let redirectUrl = button.getAttribute("data-redirect-url");
    const containerComentario = document.getElementById(
      `container-comentario-${pkComentario}`
    );
    button.addEventListener("click", (event) => {
      event.preventDefault();
      let urlEliminar = button.getAttribute("data-href");
      fetch(urlEliminar, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": getCSRFToken(),
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP Error! Status: ${response.status}`);
          }
          return response.json(); // Si la respuesta no es JSON, esto fallará
        })
        .then((data) => {
          if (data.success) {
            mensajesEliminarComentarios.innerHTML = `<p class="alert alert-primary">${data.mensaje}</p>`;
            containerComentario.remove();

            setTimeout(() => {
              window.location.href = redirectUrl;
            }, 1000);
          } else {
            mensajesEliminarComentarios.innerHTML = `<p class="alert alert-primary">${data.mensaje}</p>`;
          }
        });
    });
  });


  // Función para obtener el CSRF Token desde el HTML
  function getCSRFToken() {
    return document
      .querySelector('meta[name="csrf-token"]')
      .getAttribute("content");
  }


  //evento para eliminar respuesta a comentario
  let buttonEliminarRespuesta = document.querySelectorAll(".eliminarRespuesta");
  let mensajesEliminarRespuestas = document.querySelector(
    ".mensajes-eliminar-respuestas"
  );
  buttonEliminarRespuesta.forEach((button) => {
    let pkRespuesta = button.dataset.respuestaPk;
    let redirectUrl = button.getAttribute("data-redirect-url");
    const containerRespuesta = document.getElementById(
      `container-respuesta-${pkRespuesta}`
    );
    button.addEventListener("click", (event) => {
      event.preventDefault();
      let urlEliminarRespuesta = button.getAttribute("data-href");
      fetch(urlEliminarRespuesta, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": getCSRFToken(),
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP Error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            containerRespuesta.remove();
            mensajesEliminarRespuestas.innerHTML = `<p class="alert alert-primary">${data.mensaje}</p>`;

            setTimeout(() => {
              window.location.href = redirectUrl;
            }, 1000);
          } else {
            mensajesEliminarRespuestas.innerHTML = `<p class="alert alert-primary">${data.mensaje}</p>`;
          }
        });
    });
  });


  //evento para marcar leida las notificaciones
  let buttonNotificacion = document.querySelectorAll(".notificacion");
  buttonNotificacion.forEach((button) => {
    let notificacionPk = button.dataset.notiPk;
    const buttonNoti = document.getElementById(
      `notificacion-${notificacionPk}`
    );
    button.addEventListener("click", () => {
      let urlMarcarLeida = button.getAttribute("data-href");
      fetch(urlMarcarLeida, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(),
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            buttonNoti.classList.toggle("leida");
          }
        })
        .catch((error) => console.error("Error en la petición:", error));
    });
    const leida = button.getAttribute("data-leida");
    if (leida == "True") {
      buttonNoti.classList.toggle("leida");
    }
  });


  //evento para poder responder a un mensaje por peticion ajax
  const FormContestarMensajes = document.querySelectorAll(
    ".form-contestar-mensaje"
  );
  FormContestarMensajes.forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      let redirectUrl = form.getAttribute("data-redirect-url");
      const formData = new FormData(form); //aqui metemos todos los datos del formulario

      fetch(form.action, {
        //con esto evitamos que nos abra un json en otra pagina del navegador
        method: "POST",
        body: formData,
        header: {
          "X-Request-Width": "XMLHttpRequest", //le decimos a django que es una peticion Ajax
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            form.reset(); //con esto limpiamos el formulario

            setTimeout(() => {
              window.location.href = redirectUrl;
            }, 1000);
          } else {
          }
        });
    });
  });


  //evento para eliminar mensaje
  let buttonEliminarMensajes = document.querySelectorAll(".eliminar-mensajes");
  let mensajesEliminarMensajes = document.querySelector(
    ".mensajes-eliminar-mensajes"
  );
  buttonEliminarMensajes.forEach((button) => {
    let pkMensaje = button.dataset.mensajePk;
    let redirectUrl = button.getAttribute("data-redirect-url");
    const eliminarMensaje = document.getElementById(
      `eliminar-mensaje${pkMensaje}`
    );
    button.addEventListener("click", (event) => {
      event.preventDefault();
      let urlEliminar = button.getAttribute("data-href");
      fetch(urlEliminar, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": getCSRFToken(),
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP Error! Status: ${response.status}`);
          }
          return response.json(); // Si la respuesta no es JSON, esto fallará
        })
        .then((data) => {
          if (data.success) {
            mensajesEliminarMensajes.innerHTML = `<p class="alert alert-primary">${data.message}</p>`;

            setTimeout(() => {
              window.location.href = redirectUrl;
            }, 1000);
          } else {
            mensajesEliminarMensajes.innerHTML = `<p class="alert alert-primary">${data.message}</p>`;
          }
        });
    });
  });


  //evento para eliminar conversacion
  let buttonEliminarConversaciones = document.querySelectorAll(
    ".eliminar-conversaciones"
  );
  let mensajesEliminarConversaciones = document.querySelector(
    ".mensajes-eliminar-conversaciones"
  );
  buttonEliminarConversaciones.forEach((button) => {
    let pkConversacion = button.dataset.conversacionPk;
    let redirectUrl = button.getAttribute("data-redirect-url");
    const eliminarConversacion = document.getElementById(
      `eliminar-conversacion${pkConversacion}`
    );
    button.addEventListener("click", (event) => {
      event.preventDefault();
      let urlEliminar = button.getAttribute("data-href");
      fetch(urlEliminar, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": getCSRFToken(),
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP Error! Status: ${response.status}`);
          }
          return response.json(); // Si la respuesta no es JSON, esto fallará
        })
        .then((data) => {
          if (data.success) {
            mensajesEliminarConversaciones.innerHTML = `<p class="alert alert-primary">${data.message}</p>`;

            setTimeout(() => {
              window.location.href = redirectUrl;
            }, 1000);
          } else {
            mensajesEliminarConversaciones.innerHTML = `<p class="alert alert-primary">${data.message}</p>`;
          }
        });
    });
  });
});

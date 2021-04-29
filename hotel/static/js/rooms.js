const container = document.querySelector(".container");
const roomsContainer = document.getElementById("rooms-container");
const cheemsContainer = document.getElementById("cheems");
const reload = document.getElementById("reload");
const returnIndex = document.getElementById("reload-index");

window.addEventListener("load", async () => {
	const hotel = container.dataset.hotel_id;
	try {
		const rooms = await fetch("/api/hotel/" + hotel + "/rooms", {
			method: "GET",
		}).then((response) => response.json());

		rooms.map((el, i) => {
			roomsContainer.innerHTML += `
      <div class="room">

      <div class="header">
       <h3>${el.name}</h3>

       <div>
       <p>Codigo:</p>
       <span>#${el.room_code}</span>
       </div>

      </div>
          
        <div class="body">
           <p>Tamaño de la habitacion: ${
				el.size === "0" ? "No disponible" : el.size
			}</p>
           <h4>Instalaciones</h4>
            ${
				el.facilities.length === 0
					? `<p>Instalaciones no disponible :(</p>`
					: ""
			}
           <div class="facilities">
           <ul>
           ${el.facilities
				.map((el) => {
					return `<li data-id=${i}>${el}</li>`;
				})
				.join("")}
           </ul>
           </div>

           <div class="photos">
           ${el.photos.length === 0 ? `<p>Imagenes no disponible :(</p>` : ""}

			${el.photos.map((el) => `<img src=${el} alt=${i}/>`).join("")}
           </div>
        </div>
      </div>
	`;
		});
	} catch (e) {
		container.style.display = "none";
		cheemsContainer.style.display = "flex";
		console.log("mal salio sal algo", e);
	}

	reload.addEventListener("click", () => {
		window.location.reload();
	});

	returnIndex.addEventListener("click", () => {
		window.location.href("/");
	});
});
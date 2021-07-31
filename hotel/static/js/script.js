const hotelContainer = document.querySelector(".container");
const hotelName = document.getElementById("hotel-name");
const hotelUrl = document.getElementById("hotel-url");


const hotelLocation = document.getElementById("hotel-location");
const hotelStars = document.getElementById("hotel-stars");
const hotelImages = document.getElementById("hotel-images");
const hotelRooms = document.getElementById("hotel-rooms");
const hotelReviews = document.getElementById("hotel-reviews");
const hotelLink = document.getElementById("hotel-link");
const hotelRoomsLink = document.getElementById("hotel-rooms-link");
const cheemsContainer = document.getElementById("cheems");
const hotelForm = document.getElementById("container-form");
const loader = document.querySelector(".loader");
const reload = document.getElementById("reload");

const showHotel = (data) => {
    hotelImages.innerHTML = "";
    hotelRooms.innerHTML = "";
    hotelName.innerHTML = data.name;
    hotelLocation.innerHTML = data.direction;
    hotelStars.innerHTML = data.score + "/10";
    hotelReviews.innerHTML = data.score_review;
    hotelLink.href = data.url_page;
    hotelRoomsLink.href = "/rooms/" + data.id;
    //hotelUrl.innerHTML = `<a href="${data.url_page}"> Link </a>` 

    data.photos.map((el, i) => {
        hotelImages.innerHTML += `<img src=${el} alt=${i}/>`;
    });
    data.room.map((el, i) => {
        hotelRooms.innerHTML += `<li data-index=${i}>${el} </li>`;
    });
};

window.addEventListener("load", async () => {
    try {
        const res = await fetch("/api/hotel", {
            method: "GET",
        }).then((response) => response.json());
        showHotel(res[0]);
    } catch (e) {
        hotelContainer.style.display = "none";
        cheemsContainer.style.display = "flex";
        console.log("mal salio sal algo", e);
    }

    loader.style.opacity = "0";
    loader.style.visibility = "collapse";

    reload.addEventListener("click", () => {
        window.location.reload();
    });

    //Buscar otro hotel

    hotelForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        loader.children[0].innerHTML = "Consultando nueva busqueda";
        loader.style.opacity = "1";
        loader.style.visibility = "visible";

        const request = JSON.stringify({ url: hotelForm["url_hotel"].value });
        
        try {
            const res = await fetch("/api/hotel", {
                headers: {
                    "Content-Type": "application/json",
                },
                method: "POST",
                body: request,
            }).then((response) => response.json());
            console.log(res);
            showHotel(res);
            window.scroll(0, 0);
        } catch (e) {
            console.log(e);
            alert("Error al buscar el hotel,comprueba la url!");
        }

        hotelForm["url_hotel"].value = "";
        loader.style.opacity = "0";
        loader.style.visibility = "collapse";
    });
});
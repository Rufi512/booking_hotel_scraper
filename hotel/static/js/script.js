const hotelContainer = document.querySelector(".container");
const hotelName = document.getElementById("hotel-name");
const hotelLocation = document.getElementById("hotel-location");
const hotelStars = document.getElementById("hotel-stars");
const hotelImages = document.getElementById("hotel-images");
const hotelRooms = document.getElementById("hotel-rooms");
const hotelReviews = document.getElementById("hotel-reviews");
const hotelLink = document.getElementById("hotel-link");
const cheemsContainer = document.getElementById("cheems");
const reload = document.getElementById("reload")
window.addEventListener("load", async () => {
    try {
        const res = await fetch("/api/hotel", {
            method: "GET",
        }).then((response) => response.json());

        hotelName.innerHTML = res[0].name;
        hotelLocation.innerHTML = res[0].direction;
        hotelStars.innerHTML = res[0].score + "/10";
        hotelReviews.innerHTML = res[0].score_review;
        hotelLink.href = res[0].url_page;
        res[0].photos.map((el, i) => {
            hotelImages.innerHTML += `<img src=${el} alt=${i}/>`;
        });
        res[0].room.map((el, i) => {
            hotelRooms.innerHTML += `<li data-index=${i}>${el} </li>`;
        });
    } catch (e) {
        hotelContainer.style.display = "none";
        cheemsContainer.style.display = "flex";
        console.log("mal salio sal algo", e);
    }
});

reload.addEventListener("click",()=>{
    window.location.reload()
})

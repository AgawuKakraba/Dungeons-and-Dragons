console.log("DungeonQuest scripts loaded.");

document.addEventListener("DOMContentLoaded", function() {
    const lantern = document.createElement("div");
    lantern.classList.add("lantern");
    document.body.appendChild(lantern);

    let pos = 0;
    setInterval(() => {
        pos += 0.5;
        lantern.style.transform = `translateY(${Math.sin(pos) * 10}px)`;
    }, 20);
});
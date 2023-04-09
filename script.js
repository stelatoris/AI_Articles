function startTimer(index) {
    console.log(`Starting timer for article ${index}`);
    var time = parseInt(localStorage.getItem(`time-${index}`)) || 600;
    console.log(`Initial time for article ${index}: ${time}s`);
    var timer = setInterval(function() {
        time--;
        console.log(`Time left for article ${index}: ${time}s`);
        document.getElementById(`time-${index}`).textContent = `${time}s`;
        localStorage.setItem(`time-${index}`, time);
        if (time == 0) {
            clearInterval(timer);
            alert('Time\'s up!');
        }
    }, 1000);
}

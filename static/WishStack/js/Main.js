function startWishing() {
    var wishlistName = document.getElementById("wishlistName").value;
    if (wishlistName.trim() === "") {
        alert("Please enter a wishlist name.");
        return;
    }
    alert("Wishlist '" + wishlistName + "' created! Start adding your wishes.");
    var apiUrl = document.querySelector(".amazon-button").getAttribute("data-api-url");
    window.location.href = apiUrl; // Redirect to the API URL
}

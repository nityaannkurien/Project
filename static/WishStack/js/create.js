

const wishlistContainer = document.getElementById('wishlist-container');

function createWishlistItem() {
    const wishlistItem = document.createElement('div');
    wishlistItem.classList.add('wishlist-item');

    const buttonContainer = document.createElement('div');
    buttonContainer.classList.add('button-container');

    const message = document.createElement('span');
    message.textContent = 'Create a wishlist';
    buttonContainer.appendChild(message);

    const addButton = document.createElement('button');
    addButton.classList.add('add-button');
    addButton.textContent = '+';
    buttonContainer.appendChild(addButton);

    wishlistItem.appendChild(buttonContainer);

    wishlistContainer.appendChild(wishlistItem);
}

wishlistContainer.addEventListener('click', function (event) {
    if (event.target.classList.contains('add-button')) {
        createWishlistItem();
    }
});
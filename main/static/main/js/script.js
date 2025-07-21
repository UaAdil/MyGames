function csrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function updateCartDisplay(data) {
    const counter = document.getElementById('cart-counter');
    if (counter) counter.innerText = data.cart_items;

    const total = document.getElementById('cart-total');
    if (total) total.innerText = data.total_price + ' ₸';
}

function ajaxCart(url, pk, action) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken()
        },
        body: new URLSearchParams({ pk: pk })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'ok') {
            updateCartDisplay(data);

            const row = document.getElementById('row-' + pk);
            if (action === 'remove' || (data.quantities[pk] === 0)) {
                if (row) row.remove();
            } else {
                const qty = document.getElementById('quantity-' + pk);
                const total = document.getElementById('total-' + pk);
                if (qty) qty.innerText = data.quantities[pk];
                if (total) total.innerText = data.item_totals[pk] + ' ₸';
            }

            if (data.cart_items === 0) {
                const table = document.querySelector('table');
                const summary = document.querySelector('.text-right');
                if (table) table.remove();
                if (summary) summary.remove();

                const emptyMessage = document.createElement('p');
                emptyMessage.className = 'text-gray-600 text-lg mt-8';
                emptyMessage.innerText = 'Ваша корзина пуста.';
                document.querySelector('.container').appendChild(emptyMessage);
            }
        }
    });
}

// Actions
function addToCart(pk) { ajaxCart("/ajax/cart/add/", pk, 'add'); }
function removeFromCart(pk) { ajaxCart("/ajax/cart/remove/", pk, 'remove'); }
function increaseQty(pk) { ajaxCart("/ajax/cart/increase/", pk, 'increase'); }
function decreaseQty(pk) { ajaxCart("/ajax/cart/decrease/", pk, 'decrease'); }

// Добавление из формы
document.querySelectorAll('.add-to-cart-form').forEach(form => {
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const pk = form.querySelector('input[name="pk"]').value;
        const csrf = csrfToken();

        const response = await fetch("/ajax/cart/add/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf
            },
            body: JSON.stringify({ pk: pk })
        });

        const data = await response.json();

        if (data.status === 'ok') {
            document.getElementById('cart-counter').textContent = data.cart_items;

            const flash = document.createElement('div');
            flash.className = 'fixed top-6 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-4 py-2 rounded shadow z-50';
            flash.textContent = 'Товар добавлен в корзину';
            document.body.appendChild(flash);
            setTimeout(() => flash.remove(), 3000);
        }
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const input = document.querySelector('input[name="q"]');
    const resultsBox = document.getElementById('search-results');

    if (!input || !resultsBox) return;

    input.addEventListener('input', () => {
        const query = input.value.trim();

        if (query.length < 2) {
            resultsBox.classList.add('hidden');
            resultsBox.innerHTML = '';
            return;
        }

        fetch(`/ajax/search/?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                const results = data.results;
                resultsBox.innerHTML = '';

                if (results.length === 0) {
                    resultsBox.innerHTML = '<li class="px-4 py-2 text-sm text-gray-500">Ничего не найдено</li>';
                } else {
                    results.forEach(item => {
                        const li = document.createElement('li');
                        li.innerHTML = `
                            <a href="${item.url}" class="flex items-center gap-3 px-4 py-2 hover:bg-gray-100 hover:rounded-xl">
                                ${item.image ? `<img src="${item.image}" class="w-10 h-10 object-contain rounded" alt="">` : ''}
                                <span class="text-sm text-gray-800">${item.name}</span>
                            </a>`;
                        resultsBox.appendChild(li);
                    });
                }

                resultsBox.classList.remove('hidden');
            });
    });

    // Скрывать при клике вне поля
    document.addEventListener('click', e => {
        if (!resultsBox.contains(e.target) && e.target !== input) {
            resultsBox.classList.add('hidden');
        }
    });
});
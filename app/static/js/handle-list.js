document.addEventListener('DOMContentLoaded', function () {
    const inputItem = document.getElementById('input-item');
    const addButton = document.getElementById('add-button');
    const itemList = document.querySelector('.item-list');
    const downloadBtn = document.querySelector('.download-btn');

    function addItem() {
        const itemText = inputItem.value.trim();

        if (itemText) {
            const items = Array.from(itemList.children).map(li => li.textContent.trim());
            if (items.includes(itemText)) {
                alert('Ese link ya está en el listado');
                return;
            }

            const li = document.createElement('li');
            const span = document.createElement('span');

            span.textContent = itemText;
            li.appendChild(span);

            itemList.appendChild(li);

            inputItem.value = '';
        }
    }

    function sendListToServer() {
        const items = Array.from(itemList.children).map(li => li.textContent);

        downloadBtn.disabled = true;
        downloadBtn.textContent = 'Downloading...'

        fetch('/download-list', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ items: items })
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.message || 'Failed to download files.');
                    });
                }
                return response.json();
            })
            .then(data => {
                downloadBtn.disabled = false;
                downloadBtn.textContent = 'Download';
        
                alert(`Download completed. Files: ${data.downloaded_files.join(', ')}`);
                itemList.innerHTML = ''; 
            })
            .catch(error => {
                downloadBtn.disabled = false;
                downloadBtn.textContent = 'Download';
                
                console.error('Error:', error);
                alert(`An unexpected error occurred: ${error.message}`);
        
                itemList.innerHTML = ''; 
            });
    }

    addButton.addEventListener('click', addItem);

    inputItem.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            addItem();
        }
    });

    downloadBtn.addEventListener('click', sendListToServer);
})
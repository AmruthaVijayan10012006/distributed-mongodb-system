const output = document.getElementById('output');

const postData = async (url, data) => {
    const res = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    return res.json();
};

const putData = async (url, data) => {
    const res = await fetch(url, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    return res.json();
};

const deleteData = async (url) => {
    const res = await fetch(url, { method: 'DELETE' });
    return res.json();
};

const getData = async (url) => {
    const res = await fetch(url);
    return res.json();
};

// Insert
document.getElementById('insertForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = e.target.id.value;
    const name = e.target.name.value;
    const data = await postData('/insert', {id: parseInt(id), name});
    output.innerText = JSON.stringify(data, null, 2);
});

// Get
document.getElementById('getForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = e.target.id.value;
    const data = await getData(`/get/${id}`);
    output.innerText = JSON.stringify(data, null, 2);
});

// Update
document.getElementById('updateForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = e.target.id.value;
    const name = e.target.name.value;
    const data = await putData(`/update/${id}`, {name});
    output.innerText = JSON.stringify(data, null, 2);
});

// Delete
document.getElementById('deleteForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = e.target.id.value;
    const data = await deleteData(`/delete/${id}`);
    output.innerText = JSON.stringify(data, null, 2);
});

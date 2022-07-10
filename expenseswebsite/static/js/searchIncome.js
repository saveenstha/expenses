const searchField = document.querySelector('#searchField');

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = 'none';
const tbody = document.querySelector(".table-body");




searchField.addEventListener('keyup', (e)=>{
    const searchValue= e.target.value;

    if (searchValue.trim().length > 0){
       console.log('searchvalue', searchValue);
        paginationContainer.style.display = "none";
        tbody.innerHTML = "";
        fetch("/income/search-income/", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
        })
        .then((res)=>res.json())
        .then((data)=>{
           console.log('data', data);
           appTable.style.display="none";
           tableOutput.style.display = "block";

            if (data.length !== 0) {
                data.forEach((item) => {
                    tbody.innerHTML += `
                    <tr>
                    <td>${item.amount}</td>
                    <td>${item.source}</td>
                    <td>${item.description}</td>
                    <td>${item.date}</td>
                    </tr>`;

                });
            } else {
                tableOutput.innerHTML = 'No results Found'
            }
        });
    }else {
        tableOutput.style.display = "None"
        appTable.style.display = "block";
        paginationContainer.style.display = "block";

    }
});
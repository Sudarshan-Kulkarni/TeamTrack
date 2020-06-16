const states = [
    {'name':'karnataka'},
    {'name':'kerala'},
    {'name':'andhra pradesh'}
];

const list = document.getElementById('list');

function setList(group)
{
    clearList();
    for(const x of group)
    {
        const item = document.createElement('li');
        item.classList.add('list-group-item');
        const text = document.createTextNode(x.name);
        item.appendChild(text);
        list.appendChild(item);
    }
    if(group.length === 0)
    {
        setNoResults();
    }
}

function clearList()
{
    while(list.length>0)
        list.pop();
}

function setNoResults()
{
    const item = document.createElement('li');
        item.classList.add('list-group-item');
        const text = document.createTextNode('No Results Found');
        item.appendChild(text);
        list.appendChild(item);

}


function getPrecedence(value, searchTerm)
{
    if(value===searchTerm)
        return 2;
    else if(value.startsWith(searchTerm))
        return 1;
    else
        return 0;
}

const searchInput = document.getElementById('state');

searchInput.addEventListener('input', (event) => {
    var value = event.target.value;
    if(value && value.trim().length>0)
    {
        value = value.trim().toLowerCase();
        setList(states.filter(state => {
            return state.name.includes(value);
        }).sort((stateA, stateB) => {
            return getPrecedence(stateB.name, value) - getPrecedence(stateA.name, value);
        }));
    }
    else
    {
        clearList();
    }

    console.log()
})
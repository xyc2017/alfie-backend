function deleteExpense(expenseId){
    fetch('/delete-expense', {
        method:'POST',
        body:JSON.stringify({expenseId: expenseId})
    }).then((_res)=>{
        window.location.href="/"
    })
}
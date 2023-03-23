function deleteExpense(expenseId){
    fetch('/delete-expense', {
        method:'POST',
        body:JSON.stringify({expenseId: expenseId})
    }).then((_res)=>{
        window.location.href="/"
    })
}

function deleteGoal(goalId){
    fetch('/delete-goal', {
        method:'POST',
        body:JSON.stringify({goalId:goalId})
    }).then((_res)=>{
        window.location.href="/"
    })
}
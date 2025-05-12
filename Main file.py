create table Category(
    CategoryID int PRIMARY KEY,
    CategoryName varchar(20),
    CategoryBudget MONEY
)

create table Spending(
    TransactionID int IDENTITY(1,1) PRIMARY KEY,
    CategoryID int FOREIGN KEY REFERENCES Category(CategoryID),
    Amount MONEY,
    Date DATE
)
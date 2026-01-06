
function createProduct(name, price) {
    return {"name": name, "price": price}
}
//console.log(createProduct("apfel", 1.50))

function addProduct(shoppingBasket, product) {
    shoppingBasket.push(product)
}

function total(shoppingBasket) {
    let sum = 0;
    for (let product of shoppingBasket) {
        sum += product.price
    }
    return sum
}

function totalDiscount(shoppingBasket, discount) {
    let p = (100 - discount) / 100
    let sum = total(shoppingBasket)
    return sum * p
}

function main() {
    console.log("Hallo Phillip! :D")
    const shoppingBasket = []
    const productA = createProduct("apple", 1.5)
    const productB = createProduct("banana", 1.9)
    const productC = createProduct("coconut", 2.5)
    addProduct(shoppingBasket, productA)
    addProduct(shoppingBasket, productB)
    addProduct(shoppingBasket, productC)
    let brutto = total(shoppingBasket)
    let netto = totalDiscount(shoppingBasket, 15)
    let savings = brutto - netto
    for (let product of shoppingBasket) {
        console.log(`${product.name}: $${product.price}`)
    }
    console.log(`Your total: $${netto.toFixed(2)}. Your savings: $${savings.toFixed(2)}`)
}

main()
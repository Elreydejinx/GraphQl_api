import graphene
from graphene import ObjectType, String, Float, Int
from graphene import List, Field


class ProductType(ObjectType):
    id = Int()
    name = String()
    price = Float()
    quantity = Int()
    category = String()


products = []


class Query(ObjectType):
    products = List(ProductType)

    def resolve_products(root, info):
        return products


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = String(required=True)
        price = Float(required=True)
        quantity = Int(required=True)
        category = String(required=True)

    product = Field(ProductType)

    def mutate(root, info, name, price, quantity, category):
        product = {
            'id': len(products) + 1,
            'name': name,
            'price': price,
            'quantity': quantity,
            'category': category
        }
        products.append(product)
        return CreateProduct(product=product)

class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        price = Float()
        quantity = Int()
        category = String()

    product = Field(ProductType)

    def mutate(root, info, id, name=None, price=None, quantity=None, category=None):
        for product in products:
            if product['id'] == id:
                if name is not None:
                    product['name'] = name
                if price is not None:
                    product['price'] = price
                if quantity is not None:
                    product['quantity'] = quantity
                if category is not None:
                    product['category'] = category
                return UpdateProduct(product=product)
        return UpdateProduct(product=None)

class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = Int(required=True)

    success = graphene.Boolean()

    def mutate(root, info, id):
        global products
        products = [p for p in products if p['id'] != id]
        return DeleteProduct(success=True)

class Mutation(ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

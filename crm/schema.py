import graphene
from graphene_django import DjangoObjectType
from django.utils import timezone
from datetime import timedelta
from crm_app.models import Customer, Product, Order
from crm.models import Product


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = '__all__'


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello from GraphQL CRM!")
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)
    orders_last_week = graphene.List(OrderType)
    low_stock_products = graphene.List(ProductType)
    total_customers = graphene.Int()
    total_orders = graphene.Int()
    total_revenue = graphene.Float()

    def resolve_customers(self, info):
        return Customer.objects.all()

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_orders(self, info):
        return Order.objects.all()

    def resolve_orders_last_week(self, info):
        week_ago = timezone.now() - timedelta(days=7)
        return Order.objects.filter(order_date__gte=week_ago)

    def resolve_low_stock_products(self, info):
        return Product.objects.filter(stock__lt=10)

    def resolve_total_customers(self, info):
        return Customer.objects.count()

    def resolve_total_orders(self, info):
        return Order.objects.count()

    def resolve_total_revenue(self, info):
        total = sum(order.total_amount for order in Order.objects.all())
        return float(total) if total else 0.0


class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    success = graphene.Boolean()
    message = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []
        
        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(product)
        
        return UpdateLowStockProducts(
            success=True,
            message=f"Updated {len(updated_products)} products",
            updated_products=updated_products
        )


class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

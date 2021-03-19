import graphene

from graphene_django import DjangoObjectType
from apps.users.models import User as UserModel
from apps.decks.models import Deck as DeckModel
from apps.cards.models import Card as CardModel

class User(DjangoObjectType):
    class Meta:
        model = UserModel

class Deck(DjangoObjectType):
    class Meta:
        model = DeckModel

class Card(DjangoObjectType):
    class Meta:
        model = CardModel


class Query(graphene.ObjectType):
    users = graphene.List(User)
    decks = graphene.List(Deck)
    cards = graphene.List(Card)
    cards_by_deck = graphene.List(Card, deck_id=graphene.Int())
    deck_by_id = graphene.List(Deck, deck_id=graphene.Int())

    def resolve_users(self, info):
        return UserModel.objects.all()

    def resolve_decks(self, info):
        return DeckModel.objects.all()

    def resolve_deck_by_id(self, info, deck_id):
        return DeckModel.objects.get(id=deck_id)
    
    def resolve_cards(self, info):
        return CardModel.objects.all()

    def resolve_cards_by_deck(self, info, deck_id):
        return CardModel.objects.filter(deck_id=deck_id);

class UserCreateMutation(graphene.Mutation):
    user = graphene.Field(User)
    
    class Arguments:
        # The input arguments for this mutation
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, email, password):
        user = UserModel.objects.create(email=email, password=password)
        # Notice we return an instance of this mutation
        return UserCreateMutation(user=user)


class DeckCreateMutation(graphene.Mutation):
    deck = graphene.Field(Deck)
    
    class Arguments:
        # The input arguments for this mutation
        title = graphene.String(required=True)
        description = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, title, description):
        deck = DeckModel.objects.create(title=title, description=description)
        # Notice we return an instance of this mutation
        return DeckCreateMutation(deck=deck)

class UpdateCard(graphene.Mutation):
    card = graphene.Field(Card)
    class Arguments:
        id = graphene.ID()
        question = graphene.String()
        answer = graphene.String()

    @classmethod
    def mutate(cls, root, info, id, question, answer):
        card = CardModel.objects.get(id=id)
        card.question = question
        card.answer = answer
        card.save

        return UpdateCard(card=card)

class CardCreateMutation(graphene.Mutation):
    card = graphene.Field(Card)
    
    class Arguments:
        # The input arguments for this mutation
        question = graphene.String(required=True)
        answer = graphene.String(required=True)
        deck_id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, root, info, question, answer, deck_id):
        card = CardModel.objects.create(question=question, answer=answer, deck_id=deck_id)
        # Notice we return an instance of this mutation
        return CardCreateMutation(card=card)


class Mutation(graphene.ObjectType):
    create_user = UserCreateMutation.Field()
    create_deck = DeckCreateMutation.Field()
    create_card = CardCreateMutation.Field()
    update_card = UpdateCard.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
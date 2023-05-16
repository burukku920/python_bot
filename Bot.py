import datetime
import json
import discord
from discord.ext import commands
import threading

intents = discord.Intents.all()

class Member(discord.Member):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_entree_serveur = datetime.datetime.now()
        self.nb_commandes_utilisees = 0

    def ajouter_commande(self):
        self.nb_commandes_utilisees += 1

    def resume_activite(self):
        now = datetime.datetime.now()
        duree_presence = now - self.date_entree_serveur
        jours, heures, minutes, secondes = self._convertir_duree(duree_presence)
        resume = (
            f"Résumé de l'activité de {self.display_name}:\n"
            f"Date d'entrée dans le serveur: {self.date_entree_serveur}\n"
            f"Durée de présence: {jours} jours, {heures} heures, {minutes} minutes, {secondes} secondes\n"
            f"Nombre de commandes utilisées: {self.nb_commandes_utilisees}"
        )
        return resume


class Commande:
    def __init__(self, auteur, contenu):
        self.auteur = auteur
        self.contenu = contenu


class Noeud:
    def __init__(self, commande):
        self.commande = commande
        self.precedent = None
        self.suivant = None


class HistoriqueCommandes:
    def __init__(self):
        self.tete = None
        self.courant = None
        self.verrou = threading.Lock()

    def ajouter_commande(self, commande):
        with self.verrou:
            nouveau_noeud = Noeud(commande)

            if self.tete is None:
                self.tete = nouveau_noeud
                self.courant = nouveau_noeud
            else:
                nouveau_noeud.precedent = self.courant
                self.courant.suivant = nouveau_noeud
                self.courant = nouveau_noeud
    def vider_historique(self):
        with self.verrou:
            self.tete = None
            self.courant = None

    def obtenir_derniere_commande(self):
        with self.verrou:
            if self.courant is not None:
                return self.courant.commande
            else:
                return None

    def obtenir_commandes_utilisateur(self, utilisateur):
        with self.verrou:
            commandes_utilisateur = []
            noeud = self.tete

            while noeud is not None:
                if noeud.commande.auteur == utilisateur:
                    commandes_utilisateur.append(noeud.commande)
                noeud = noeud
                if noeud is not None:
                    return self.courant.commande
                else:
                    return None

    def obtenir_commandes_utilisateur(self, utilisateur):
        with self.verrou:
            commandes_utilisateur = []
            noeud = self.tete

            while noeud is not None:
                if noeud.commande.auteur == utilisateur:
                    commandes_utilisateur.append(noeud.commande)
                noeud = noeud.suivant

            return commandes_utilisateur
    def deplacer_en_arriere(self):
        with self.verrou:
            if self.courant is not None and self.courant.precedent is not None:
                self.courant = self.courant.precedent

    def deplacer_en_avant(self):
        with self.verrou:
            if self.courant is not None and self.courant.suivant is not None:
                self.courant = self.courant.suivant
        


class Bot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix, intents=intents)
        self.historique_commandes = HistoriqueCommandes()
        self.donnees_utilisateur = {}

    @staticmethod
    def _obtenir_membre(guild, author):
        member = guild.get_member(author.id)
        return member
    

    async def on_ready(self):
        print(f'Bot connecté en tant que {self.user.name}')

    @staticmethod
    def _obtenir_membre(guild, author):
        member = guild.get_member(author.id)
        return member



    @commands.command()
    async def resume(self, ctx):
        membre = self._obtenir_membre(ctx.guild, ctx.author)
        resume = membre.resume_activite()
        await ctx.send(resume)

    @commands.command()
    async def historique(self, ctx):
        membre = self._obtenir_membre(ctx.guild, ctx.author)
        commandes_utilisateur = self.historique_commandes.obtenir_commandes_utilisateur(membre)
        historique = [commande.contenu for commande in commandes_utilisateur]
        await ctx.send(historique)

    async def on_command_completion(self, ctx):
        membre = self._obtenir_membre(ctx.guild, ctx.author)
        membre.ajouter_commande()
        commande = Commande(membre, ctx.message.content)
        self.historique_commandes.ajouter_commande(commande)
        
bot = Bot(command_prefix="!",)

@bot.event
async def on_ready():
    print("Bot prêt")



@bot.event
async def on_member_join(member):
    general_channel = bot.get_channel(1044900412551073832)
    await general_channel.send(f"Bienvenue sur le serveur, {member.name}!")

@bot.command(name="lastCommand")
async def last_command(ctx):
    derniere_commande = bot.historique_commandes.obtenir_derniere_commande()
    if derniere_commande is None:
        await ctx.send("Aucune commande dans l'historique.")
        return

    await ctx.send(f"Dernière commande : {derniere_commande.auteur}: {derniere_commande.contenu}")

@bot.command(name="moveL")
async def move_left(ctx):
    bot.historique_commandes.deplacer_en_arriere()
    await ctx.send("Position dans l'historique déplacée vers la commande précédente.")

@bot.command(name="moveR")
async def move_right(ctx):
    bot.historique_commandes.deplacer_en_avant()
    await ctx.send("Position dans l'historique déplacée vers la commande suivante.")

@bot.command(name="binH")
async def bin_history(ctx):
    bot.historique_commandes.vider_historique()
    await ctx.send("Historique des commandes vidé.")

@bot.command(name="reset")
async def reset(ctx):
    identifiant_utilisateur = str(ctx.author.id)
    bot.donnees_utilisateur.pop(identifiant_utilisateur, None)
    await ctx.send("Conversation réinitialisée.")

@bot.command(name="speakA")
async def speak_about_x(ctx, sujet):
    identifiant_utilisateur = str(ctx.author.id)
    donnees_utilisateur = bot.donnees_utilisateur.get(identifiant_utilisateur, {})
    if sujet in donnees_utilisateur:
        await ctx.send(f"Le bot parle de {sujet}.")
    else:
        await ctx.send(f"Le bot ne parle pas de {sujet}.")

bot.run("MTA5MTI2MTQwNjY4NDM4NTM1MA.GVmsiL.4RXQ5cL7B8xZpgHkTsOiNDqGeZoD1VyNpMCgWY")
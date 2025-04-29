import streamlit as st

def calculer_capacite_emprunt(revenu, depenses, taux_interet, duree_pret, taux_endettement):
    # Calcul de la capacité d'emprunt mensuelle en fonction du taux d'endettement
    mensualite = (revenu - depenses) * (taux_endettement / 100)
    # Calcul du montant total empruntable
    if taux_interet > 0:
        capacite_emprunt = mensualite * ((1 - (1 + taux_interet / 12) ** (-duree_pret * 12)) / (taux_interet / 12))
    else:
        capacite_emprunt = mensualite * duree_pret * 12
    return capacite_emprunt, mensualite

def calculer_frais_notaire(capacite_emprunt, type_bien):
    # Frais de notaire : environ 7-8% pour l'ancien, 2-3% pour le neuf
    if type_bien == "Ancien":
        frais_notaire = capacite_emprunt * 0.08
    elif type_bien == "Neuf":
        frais_notaire = capacite_emprunt * 0.03
    else:
        frais_notaire = 0
    return frais_notaire

# Titre de l'application
st.title("Simulation de Capacité d'Emprunt")

# Entrées utilisateur
st.header("Informations financières")
col1, col2 = st.columns(2)
with col1:
    revenu = st.number_input("Revenu mensuel (€)", min_value=0.0, step=100.0)
with col2:
    depenses = st.number_input("Dépenses mensuelles (€)", min_value=0.0, step=100.0)
apport = st.number_input("Apport financier (€)",min_value=0.0, step=100.0)
duree_pret = st.number_input("Durée du prêt (années)", min_value=1, step=1)
taux_interet = st.slider("Taux d'intérêt annuel (%)", min_value=0.0, max_value=10.0, step=0.1) / 100
taux_endettement = st.slider("Taux d'endettement (%)", min_value=1, max_value=35, value=35)

# Type de bien
st.header("Type de bien")

type_bien = st.radio("Sélectionnez le type de bien :", ("Ancien", "Neuf"))
montant_travaux = st.number_input("Montant des travaux (€)", min_value=0.0, step=100.0)

# Bouton pour lancer la simulation
if revenu > depenses:
    capacite_emprunt, mensualite = calculer_capacite_emprunt(revenu, depenses, taux_interet, duree_pret, taux_endettement)
    remboursement_total = mensualite * duree_pret * 12  # Calcul du montant total remboursé
    frais_notaire = calculer_frais_notaire(capacite_emprunt-montant_travaux, type_bien)  # Calcul des frais de notaire
    frais_garantie = capacite_emprunt*0.008

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"Votre capacité d'emprunt est estimée à : {capacite_emprunt:,.2f} €")
        st.info(f"Vous devrez rembourser environ : {mensualite:,.2f} € par mois.")
        st.error(f"Le montant total remboursé sur {duree_pret} ans sera de : {remboursement_total:,.2f} €")
    with col2:
        st.success(f"Compte en banque à {apport+capacite_emprunt:,.2f} €")
        st.info(f"Les frais de notaire pour un bien {type_bien.lower()} sont estimés à : {frais_notaire:,.2f} €")
        st.info(f"Les frais de garanties sont estimés à {frais_garantie:,.2f} €")
    
    st.success(f"Une proposition judicieuse serait de {apport+capacite_emprunt-frais_garantie-frais_notaire:,.2f} €")

else:
    st.error("Les dépenses doivent être inférieures aux revenus pour calculer la capacité d'emprunt.")
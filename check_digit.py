from collections import deque


def modulo_10_ricorsivo(trial_number):
    row_0 = (0, 9, 4, 6, 8, 2, 7, 1, 3, 5)
    carry_over = 0
    """
    Funzione per calcolare il modulo 10 ricorsivo.
    row_0 è la sequenza ufficiale per il calcolo del modulo 10 trovata sull'Annex B delle Swiss Implementation Guidelines for the QR-bill
    In realtà sull'annex B è una matrice, ma è sempre la stessa sequenza shiftata.
    Per shiftare usa le collections che sono fatte apposta per questo genere di cose.
    """
    for number in trial_number:
        # Si parte sempre dalla stessa base che è row_0 e si crea una deque che è un contenitore che offre metodi per shiftare i numeri
        a = deque(row_0)
        # Si shifta la deque con il metodo rotate() del numero di carry_over (negativo per shiftare nella direzione giusta, la partenza è zero)
        a.rotate(-1*carry_over)
        # Si determina il nuovo carry_over (che si utilizza nel giro successivo) accedendode al contenuto della deque shiftata con la indice la cifra che si sta esaminando
        carry_over = a[int(number)]
    check_digit = 10-carry_over
    return check_digit if check_digit < 10 else 0


trial_number = '00440012224340297939443407'
print(modulo_10_ricorsivo(trial_number))


def verify_luhn(n):
    """
    Funzione per controllare se il check digit che viene passato insieme al numero in ultima posizione è corretto
    """
    r = [int(ch) for ch in str(n)][::-1]
    # print(r)
    return (sum(r[0::2]) + sum(sum(divmod(d*2, 10)) for d in r[1::2])) % 10 == 0


for n in (49927398716, 49927398717, 1234567812345678, 1234567812345670):
    print(n, verify_luhn(n))


def check_luhn(n, with_check_digit=True):
    """
    Funzione per verificare calcolare il check digit di luhn 
    with_check_digit=True se il numero che viene passato lo contiene in ultima posizione (default), false se non lo contiene

    """
    # print(n)
    r = [int(ch) for ch in str(n)]
    if with_check_digit:
        r = r[:-1]
    # print(r)
    r = r[::-1]
    # print(r)
    result = (sum(r[1::2]) + sum(sum(divmod(d*2, 10)) for d in r[0::2])) % 10
    return 10-result if result != 0 else result


for n in (49927398716, 49927398717, 1234567812345678, 1234567812345670):
    print(n, check_luhn(n, True))

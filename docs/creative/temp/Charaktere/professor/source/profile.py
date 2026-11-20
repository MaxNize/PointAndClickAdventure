"""Parametrischer Profil-Generator (Seitenansicht des Gesichts, Blick nach rechts).
Gleicher Stil wie das abgestimmte Profil der Alchemistin: senkrechte Stirn, kleine Delle an der
Nasenwurzel, stilisierte Nase, kleine Lippenkerbe, Kinn, Kieferbogen zum Hals.
Hinterkopf/Hals-Anschluss ist bei allen Varianten identisch -> Haare/Hüte passen weiter."""

def profile(fx=245.5, dent=1.8, nose="pointy", L=11, ty=160, lip=252, chin=248, cy=198,
            jaw="soft", jx=212, double=False, **_):
    R = (fx - dent, 150.5)          # Nasenwurzel
    T = (fx + L, ty)                # Nasenspitze
    d = (f"M162,140 C162,102 186,96 200,96.5 C215,96.8 230,104 239,114 "
         f"C{fx-2},119 {fx},124 {fx},130 L{fx},143 C{fx},146.5 {R[0]},148 {R[0]},{R[1]} ")
    # Nasenrücken
    if nose == "straight":
        d += f"C{R[0]+1},{R[1]+3} {T[0]-2},{T[1]-4} {T[0]},{T[1]} "
    elif nose == "hook":
        d += f"C{R[0]+L*0.55},{R[1]-1.5} {T[0]+1.5},{T[1]-7} {T[0]},{T[1]} "
    elif nose == "upturned":
        T = (T[0], T[1] - 2)
        d += f"C{R[0]+1},{R[1]+6} {T[0]-5},{T[1]+2} {T[0]},{T[1]} "
    elif nose == "button":
        d += (f"C{R[0]+1},{R[1]+5} {T[0]-5},{T[1]-3} {T[0]-2.5},{T[1]-2} "
              f"Q{T[0]+2},{T[1]} {T[0]-0.5},{T[1]+3} ")
        T = (T[0] - 0.5, T[1] + 1)
    else:  # pointy (Anime-Standard)
        d += f"C{R[0]+2},{R[1]+4} {T[0]-3},{T[1]-2.5} {T[0]},{T[1]} "
    # Nasenunterseite -> Oberlippe -> Mundkerbe -> Unterlippe
    N = (lip - 0.8, T[1] + 7)
    U = (lip, N[1] + 5)
    M = (lip - 2.6, U[1] + 2.8)
    Lo = (lip - 0.9, M[1] + 3.4)
    D = (chin - 1.6, Lo[1] + 4.5)
    C1 = (chin, cy - 5)
    d += (f"L{T[0]-0.6},{T[1]+2.2} C{T[0]-2.5},{T[1]+5} {N[0]+2},{N[1]-1} {N[0]},{N[1]} "
          f"C{N[0]},{N[1]+2} {U[0]},{U[1]-3} {U[0]},{U[1]} L{M[0]},{M[1]} "
          f"C{M[0]+1.6},{M[1]+1} {Lo[0]},{Lo[1]-2} {Lo[0]},{Lo[1]} "
          f"C{Lo[0]},{Lo[1]+2} {D[0]+1},{D[1]-2} {D[0]},{D[1]} "
          f"C{D[0]},{D[1]+2} {C1[0]},{C1[1]-3} {C1[0]},{C1[1]} ")
    # Kinn
    if jaw == "square":
        d += f"L{chin},{cy-1} L{chin-4},{cy} "
    elif jaw == "round":
        d += f"C{chin},{cy-1} {chin-3},{cy+0.5} {chin-8},{cy+0.5} "
    else:
        d += f"C{chin},{cy-2} {chin-2},{cy} {chin-6},{cy} "
    if double:
        d += f"C{chin-9},{cy+5} {chin-20},{cy+7} {chin-28},{cy+4} "
    # Kiefer -> Hals (Anschluss wie im Originalprofil)
    if jaw == "square":
        d += f"L{jx},{cy+0.5} L{jx-6},{cy-4} C206,{cy-6} 203.5,191.5 201.5,188 "
    else:
        d += f"L{jx},{cy+0.3} C{jx-5},{cy} 204,193 201.5,188 "
    d += "C200,185 199,183 197.5,182 C190,184 176,178 168,166 C162,158 162,150 162,140 Z"
    mouth = f"M{M[0]+0.6},{M[1]} Q{M[0]-2.4},{M[1]+0.8} {M[0]-5},{M[1]+0.2}"
    return {"d": d, "mouth": mouth, "nose_tip": T}

PRESETS = {
    # NPCs
    "lena":      dict(nose="button",   L=7,  ty=159, lip=251, chin=246.5, cy=195, jaw="round", jx=212),
    "tobi":      dict(nose="straight", L=10, ty=161, lip=252, chin=249,   cy=199, jaw="soft",  jx=214),
    "grombart":  dict(nose="button",   L=13, ty=164, lip=250.5, chin=246, cy=200, jaw="round", jx=212, double=True),
    "seidel":    dict(nose="pointy",   L=13, ty=162, lip=251, chin=246,   cy=196, jaw="soft",  jx=211, fx=244.5),
    "maren":     dict(nose="upturned", L=9,  ty=160, lip=252, chin=247.5, cy=196, jaw="round", jx=212),
    "fynn":      dict(nose="button",   L=6,  ty=158, lip=250, chin=245.5, cy=194, jaw="round", jx=211, fx=244.5),
    "brandt":    dict(nose="hook",     L=14, ty=164, lip=250, chin=245,   cy=197, jaw="soft",  jx=211),
    "ilse":      dict(nose="straight", L=11, ty=162, lip=252.5, chin=248.5, cy=198, jaw="round", jx=213),
    "kurt":      dict(nose="straight", L=13, ty=163, lip=253, chin=252.5, cy=203, jaw="square", jx=219, fx=246.5),
    "yara":      dict(nose="pointy",   L=10, ty=160, lip=252, chin=248,   cy=196, jaw="soft",  jx=212),
}

def preset(name):
    return profile(**PRESETS[name])

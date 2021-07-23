import pygame
from pygame.locals import *
import random
import sys

#Esta version no puede tener try-catch, clases, ni nada que no hayan visto fuera del ramo, sin contar metodos de pygame
#Todo el arte está sacado de internet
#Por algun motivo, al poner el x y la y, se tiene que hacer [y][x] y no [x][y]

#================================================================
#                       Crea Matrix
#================================================================
def creaMatrix(n):
    
    matriz = []
    linea = []
    
    for i in range(n):
        linea = [] #linea parte vacia por iteracion
        for j in range(n): #Agrega n 0s a linea
            linea.append(0) 
        matriz.append(linea) #Agrega linea a matriz
        
    return matriz #resulta una matriz de n listas con n 0s cada una

#================================================================
#                       Validacion movimientos
#================================================================

def movimiento(posicionActual, sentido, posicionActualMatriz, largo, pixeles, amigo, matrix, eje, segundaCoordenada):

    posicionActual += pixeles #Se mueve pixeles px dependiendo del signo
    posicionActualMatriz += sentido #Se mueve sentido valores de la matriz dependiendo del signo
    mov = True #Ve si de verdad se movio, o si se mantivo en el lugar
    
    if (amigo):
    
        #No puede salir del tablero ni pisar un obstaculo
        if ((posicionActualMatriz >= largo or posicionActualMatriz < 0 ) or (eje == 'y' and matrix[posicionActualMatriz][segundaCoordenada] == 2) or (eje == 'x' and matrix[segundaCoordenada][posicionActualMatriz] == 2)):#or lugar == 2 ): #Validacion para que no se salga del tablero
            posicionActual -= pixeles
            posicionActualMatriz -= sentido
            mov = False        
            
        return posicionActual, posicionActualMatriz, mov
            
    #No puede salir del tablero ni pisar un obstaculo, pero da igual si se mueve o no
    if (posicionActualMatriz >= largo or posicionActualMatriz < 0 or (eje == 'y' and matrix[posicionActualMatriz][segundaCoordenada] == 2) or (eje == 'x' and matrix[segundaCoordenada][posicionActualMatriz] == 2)): #Validacion para que no se salga del tablero
            posicionActual -= pixeles
            posicionActualMatriz -= sentido
    return posicionActual, posicionActualMatriz
    
#================================================================
#                       Chequea Ganar
#================================================================

def pintado(matrix, dim):
    
    for i in range(dim):
        if (matrix[i].count(0) > 0):
            return False
    
    return True

#================================================================
#                       Genera posicion inicial
#================================================================

def generaPos0(matX,matY, dimX, dimY, margen, altoCuad, anchoCuad):

    pos_x = margen + ((anchoCuad + margen) * matX) + anchoCuad//2 - dimX//2 #Posicion inicial en x
    pos_y = margen + ((altoCuad + margen) * matY) + altoCuad//2 - dimY//2 #Posicion inicial en y
    pos_cuad_x = matX #Posicion inicial en cuadricula en x
    pos_cuad_y = matY #Posicion inicial en cuadricula en y
    
    return pos_x, pos_y, pos_cuad_x, pos_cuad_y

#================================================================
#                   Genera posicion aleatoria bloque
#================================================================

def posAleatoria(dimensionM):


        pos_x = random.randrange(1,dimensionM)   
        pos_y = random.randrange(1,dimensionM)
        
        return pos_x,pos_y
        
#================================================================
#                   Despliega Tablero
#================================================================
        
def despliegaTablero(bloquePintado, bloqueDespintado, bloqueObstaculo, cuadricula):

    for fila in range(10):
        for columna in range(10):
        
            imagen = bloqueDespintado
            
            if cuadricula[fila][columna] == 1: #Cambia de valor cuando qbert lo pisa
                imagen = bloquePintado
            
            elif cuadricula[fila][columna] == 2: #A no ser que sea un obstaculo
                imagen = bloqueObstaculo
            
            pantalla.blit(imagen, ((margen+ancho) * columna + margen, (margen+alto) * fila + margen))
        
#================================================================
#                   Animaciones
#================================================================
    
def animacion(nFrames, assets, coordenadas):
    #for i in range(nFrames):
    pantalla.blit(assets[0], (coordenadas[0],coordenadas[1]))
    pygame.display.flip()
    pygame.time.wait(200)

#================================================================
#                   Valida obstaculos
#================================================================

def obstaculosCorrectos(x,y,matrix):

    if (x == 1 and y == 1 or x >= len(matrix) or y >= len(matrix) or matrix[x][y] == 2): #Se vuelve a hacer porque o si no podria estar en el 0,0
        return False
    return True
    
#================================================================
#                   Genera obstaculos
#================================================================

def generaObstaculos(listaInicialObs, matrix):
          
    cont = 0
    listaRespaldo = listaInicialObs[:]

    while cont < len(listaInicialObs):
    
        if cont == 0:
            obstaculo_pos_x, obstaculo_pos_y = posAleatoria(len(matrix)-1)
            
        
        listaInicialObs[cont] += obstaculo_pos_x
        listaInicialObs[cont+1] += obstaculo_pos_y
        
        if not (obstaculosCorrectos(listaInicialObs[cont],listaInicialObs[cont+1], matrix)):

            cont = 0
            listaInicialObs = listaRespaldo[:]

        else:
            cont += 2      
            
    for i in range(0, len(listaInicialObs), 2):
        matrix[listaInicialObs[i]][listaInicialObs[i+1]] = 2
                
    return matrix

#================================================================
#                   Pantalla instrucciones
#================================================================

def pantallaInstrucciones():

    instrucciones = pygame.image.load("instrucciones.png").convert()
    pantalla.blit(instrucciones, (0,0))
    pygame.display.flip()
    
    corriendo = True
    while corriendo:
        for event in pygame.event.get():
            
                if (event.type == pygame.QUIT):
                    corriendo = False
                
                #Controlar jugador1
                elif (event.type == pygame.KEYDOWN):
                    
                    if event.key == K_SPACE: #mueve hacia arriba
                        main()  
                            
                            
                    elif event.key == K_ESCAPE: #mueve hacia arriba
                        corriendo = False    

    sys.exit()

#================================================================
#                   Nivel principal
#================================================================
    
def nivelPrincipal(pantalla, margen, dimensionMatrix, ancho, alto, clock, fondo, bloquePintado, bloqueDespintado, bloqueObstaculo, qbert, enemigo1, enemigo2, frames, animacionMuerte, fuente):

    vidas = 2
    puntaje = 50000
    reiniciar = False
    #Setear cuadricula----------------------------------------------
    
    cuadricula = creaMatrix(dimensionMatrix)
    cuadricula[0][0] = 1 #0,0 siempre marcado
    
    
    #Obstaculos-----------------------------------------------------
    
    cuadricula = generaObstaculos([1,1], cuadricula)
    cuadricula = generaObstaculos([0,1,1,1], cuadricula)
    cuadricula = generaObstaculos([1,0,1,1,2,0], cuadricula)
    
    
    #Player----------------------------------------------------------
    
    altoQbert = qbert.get_height() 
    anchoQbert = qbert.get_width() 
    qbert_pos_x, qbert_pos_y, qbert_pos_cuad_x, qbert_pos_cuad_y = generaPos0(0, 0, anchoQbert, altoQbert, margen, alto, ancho) #Posicion inicial
    
    
    #Enemigo1--------------------------------------------------------
    
    altoEnemigo1 = enemigo1.get_height() 
    anchoEnemigo1 = enemigo1.get_width() 
    enemigo1_pos_x, enemigo1_pos_y,  enemigo1_pos_cuad_x, enemigo1_pos_cuad_y = generaPos0(random.randrange(1,dimensionMatrix), random.randrange(1,dimensionMatrix), anchoEnemigo1, altoEnemigo1, margen, alto, ancho) #Posisicon inicial

    while (cuadricula[enemigo1_pos_cuad_y][enemigo1_pos_cuad_x] == 2):
        enemigo1_pos_x, enemigo1_pos_y,  enemigo1_pos_cuad_x, enemigo1_pos_cuad_y = generaPos0(random.randrange(1,dimensionMatrix), random.randrange(1,dimensionMatrix), anchoEnemigo1, altoEnemigo1, margen, alto, ancho) #Posisicon inicial
    
    
    #Enemigo2--------------------------------------------------------
    
    altoEnemigo2 = enemigo2.get_height() 
    anchoEnemigo2 = enemigo2.get_width() 
    enemigo2_pos_x, enemigo2_pos_y,  enemigo2_pos_cuad_x, enemigo2_pos_cuad_y = generaPos0(random.randrange(1,dimensionMatrix), random.randrange(1,dimensionMatrix), anchoEnemigo2, altoEnemigo2, margen, alto, ancho) #Posisicon inicial
    
    while (cuadricula[enemigo2_pos_cuad_y][enemigo2_pos_cuad_x] == 2 or (enemigo2_pos_cuad_x == enemigo1_pos_cuad_x and enemigo2_pos_cuad_y == enemigo1_pos_cuad_y)):
        enemigo2_pos_x, enemigo2_pos_y,  enemigo2_pos_cuad_x, enemigo2_pos_cuad_y = generaPos0(random.randrange(1,dimensionMatrix), random.randrange(1,dimensionMatrix), anchoEnemigo2, altoEnemigo2, margen, alto, ancho) #Posisicon inicial
    
    #Colocar assets--------------------------------------------------
    
    pantalla.blit(fondo, (0,0)) #en posicion 0,0 de la ventana 
    pantalla.blit(qbert, (qbert_pos_x,qbert_pos_y)) #la vaca se llama qbert
    pantalla.blit(enemigo1, (enemigo1_pos_x,enemigo1_pos_y))
    pantalla.blit(enemigo2, (enemigo2_pos_x,enemigo2_pos_y))
    
    pygame.display.flip()
    
    # el bucle principal del juego
    corriendo = True
    while corriendo and not reiniciar:
            
        #Tiene que estar antes que el spawn del tablero para que se pueda ver
        pantalla.blit(fondo, (0,0))
        
        #Texto--------------------------------------------------------------
        vidasTxt = fuente.render(str(vidas), True, (255,255,255))
        vidasTxtRect = vidasTxt.get_rect()
        vidasTxtRect.center = (975, 120)
        pantalla.blit(vidasTxt, vidasTxtRect)
        
        puntajeTxt = fuente.render(str(puntaje), True, (255,255,255))
        puntajeTxtRect = puntajeTxt.get_rect()
        puntajeTxtRect.center = (990, 310)
        pantalla.blit(puntajeTxt, puntajeTxtRect)
        
        despliegaTablero(bloquePintado, bloqueDespintado, bloqueObstaculo, cuadricula)
        clock.tick(60) #Para que el juego corra a 60 FPS independiente de los componentes del computador
        
        mov = False #Evita que los enemiugos se muevan al presionar cualquier tecla que no sea para avanzar
        
        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
        
            if (event.type == pygame.QUIT): #Al presionar X (el boton, no la tecla), se cierra el juego
                sys.exit(0)
            
            elif (event.type == pygame.KEYDOWN):
                
                #Mientras qbert se mueve en la pantalla, tambien se mueve en la matriz
                
                if event.key == K_ESCAPE: #Segunda opcion para cerrar
                    sys.exit(0)
                    
                elif event.key == K_r: #Resetea el nivel
                    reiniciar = True
                    
                elif event.key == K_g:
                    print(pygame.mouse.get_pos())
                    
                if (vidas > 0):
                
                    #Controlar jugador1
                    if event.key == K_w: #mueve hacia arriba
                        qbert_pos_y, qbert_pos_cuad_y, mov = movimiento(qbert_pos_y, -1, qbert_pos_cuad_y, dimensionMatrix, -(margen + alto), True, cuadricula, 'y', qbert_pos_cuad_x)
                        
                    elif event.key == K_s: #mueve hacia abajo
                        qbert_pos_y, qbert_pos_cuad_y, mov = movimiento(qbert_pos_y, 1, qbert_pos_cuad_y, dimensionMatrix, margen + alto, True, cuadricula, 'y', qbert_pos_cuad_x)
                           
                    elif event.key == K_a: #mueve hacia la izquierda
                        qbert_pos_x, qbert_pos_cuad_x, mov = movimiento(qbert_pos_x, -1, qbert_pos_cuad_x, dimensionMatrix, -(margen + ancho), True, cuadricula, 'x', qbert_pos_cuad_y)
                        
                    elif event.key == K_d:  #mueve hacia la derecha
                        qbert_pos_x, qbert_pos_cuad_x, mov = movimiento(qbert_pos_x, 1, qbert_pos_cuad_x, dimensionMatrix, margen + ancho, True, cuadricula, 'x', qbert_pos_cuad_y)
                        

                if mov: #if que comprueba si se movio despues del turno, para mover los enemigos solo cuando sea necesario

                    puntaje -= 10
                
                    cuadricula[qbert_pos_cuad_y][qbert_pos_cuad_x] = not(cuadricula[qbert_pos_cuad_y][qbert_pos_cuad_x]) #Cambia estado del lugar en la matrix (pasto -> arbol, arbol -> pasto)
                    
                    #Movimiento enemigos
                    mueveX1 = random.randint(0,1)    #Decide si se mueve en X o Y
                    mueveX2 = random.randint(0,1)
                    movEnemigo1 = random.choice([-1,1]) #Decide hacia que sentido se mueve
                    movEnemigo2 = random.choice([-1,1])
                    
                    if (mueveX1):
                        enemigo1_pos_x, enemigo1_pos_cuad_x = movimiento(enemigo1_pos_x, movEnemigo1, enemigo1_pos_cuad_x, dimensionMatrix, (margen + ancho)*movEnemigo1, False, cuadricula, 'x', enemigo1_pos_cuad_y) #mueve en X
                        
                    else:
                        enemigo1_pos_y, enemigo1_pos_cuad_y = movimiento(enemigo1_pos_y, movEnemigo1, enemigo1_pos_cuad_y, dimensionMatrix, (margen + alto)*movEnemigo1, False, cuadricula, 'y', enemigo1_pos_cuad_x) #mueve en Y
                        
                    if (enemigo1_pos_cuad_x == 0 and enemigo1_pos_cuad_y == enemigo1_pos_cuad_x):  #El enemigo1 nunca puede estar en (0,0)
                        enemigo1_pos_cuad_x += 1 
                        enemigo1_pos_x += margen + ancho
                        
                    if (mueveX2):
                        enemigo2_pos_x, enemigo2_pos_cuad_x = movimiento(enemigo2_pos_x, movEnemigo2, enemigo2_pos_cuad_x, dimensionMatrix, (margen + ancho)*movEnemigo2, False, cuadricula, 'x', enemigo2_pos_cuad_y) #mueve en X
                        
                    else:
                        enemigo2_pos_y, enemigo2_pos_cuad_y = movimiento(enemigo2_pos_y, movEnemigo2, enemigo2_pos_cuad_y, dimensionMatrix, (margen + alto)*movEnemigo2, False, cuadricula, 'y', enemigo2_pos_cuad_x) #mueve en Y
                        
                    while (enemigo2_pos_cuad_x == enemigo1_pos_cuad_x and enemigo2_pos_cuad_y == enemigo1_pos_cuad_y):
                        mueveX2 = random.randint(0,1)   
                        movEnemigo2 = random.choice([-1,1])
                        if (mueveX2):
                            enemigo2_pos_x, enemigo2_pos_cuad_x = movimiento(enemigo2_pos_x, movEnemigo2, enemigo2_pos_cuad_x, dimensionMatrix, (margen + ancho)*movEnemigo2, False, cuadricula, 'x', enemigo2_pos_cuad_y) #mueve en X
                            
                        else:
                            enemigo2_pos_y, enemigo2_pos_cuad_y = movimiento(enemigo2_pos_y, movEnemigo2, enemigo2_pos_cuad_y, dimensionMatrix, (margen + alto)*movEnemigo2, False, cuadricula, 'y', enemigo2_pos_cuad_x) #mueve en Y
                            
                        
                    if (enemigo2_pos_cuad_x == 0 and enemigo2_pos_cuad_y == enemigo2_pos_cuad_x):  #El enemigo2 nunca puede estar en (0,0)
                        enemigo2_pos_cuad_x += 1 
                        enemigo2_pos_x += margen + ancho
                        
                    if ((enemigo1_pos_cuad_y == qbert_pos_cuad_y and enemigo1_pos_cuad_x == qbert_pos_cuad_x) or (enemigo2_pos_cuad_y == qbert_pos_cuad_y and enemigo2_pos_cuad_x == qbert_pos_cuad_x)): #Qbert muere
                        
                        vidas -= 1
                        animacion(frames, animacionMuerte, (qbert_pos_x,qbert_pos_y))                                
                        qbert_pos_x, qbert_pos_y, qbert_pos_cuad_x, qbert_pos_cuad_y = generaPos0(0, 0, anchoQbert, altoQbert, margen, alto, ancho) #Posicion inicial
                        
                        
                    if (pintado(cuadricula, dimensionMatrix)): #Qbert gana

                        return False, True, puntaje*vidas
              
            
        if (vidas > 0):
        # actualizamos la pantalla
            pantalla.blit(qbert, (qbert_pos_x,qbert_pos_y))
            pantalla.blit(enemigo1, (enemigo1_pos_x,enemigo1_pos_y))
            pantalla.blit(enemigo2, (enemigo2_pos_x,enemigo2_pos_y))
            pygame.display.flip()
            
        else:
            return False, False, puntaje*vidas
            
        if reiniciar:
            return True, False, 0

            
#================================================================
#                   Pantalla de derrota o ganador
#================================================================    

def final(ganador, pantallaGanador, pantallaPerdedor, puntos, fuente):
    if ganador:
    #Imprime pantalla victoria
        pantalla.blit(pantallaGanador, (0,0))
        
        puntajeTxt = fuente.render(str(puntos), True, (255,255,255))
        puntajeTxtRect = puntajeTxt.get_rect()
        puntajeTxtRect.center = (914, 728)
        pantalla.blit(puntajeTxt, puntajeTxtRect)
        
    else:
    #imprime pantalla derrota
        pantalla.blit(pantallaPerdedor, (0,0))
    
    pygame.display.flip()
    corriendo = True
    
    while corriendo:
        for event in pygame.event.get():
            
                if (event.type == pygame.QUIT):
                    corriendo = False
                
                #Controlar jugador1
                elif (event.type == pygame.KEYDOWN):
                    
                    if event.key == K_r or event.key == K_SPACE: 
                        main()
                            
                            
                    elif event.key == K_ESCAPE: 
                        corriendo = False   
    sys.exit(0)
    
        
#================================================================
#                       Funcion principal
#================================================================
pygame.init()

margen = 5 #Espacio entre cuadraditos
dimensionMatrix = 10
ancho = 80 #ancho cuadrado
alto = ancho #Alto cuadrado

pantalla_WIDTH = 1155
pantalla_HEIGHT = 855
pantalla = pygame.display.set_mode((pantalla_WIDTH, pantalla_HEIGHT))
pygame.display.set_caption("Testing Qbert")
clock = pygame.time.Clock()
pygame.key.set_repeat(500, 50) #Para permitir la repeticion de teclas, primer parametro es cuanto se demora en milisegundos la primera, y el segundo el resto

    
def main():

    
    #Cargar imagenes
    fondo = pygame.image.load("fondo.png").convert()
    bloquePintado = pygame.image.load("bloquePintado.png").convert_alpha()
    bloqueDespintado = pygame.image.load("bloqueDespintado.png").convert_alpha()
    bloqueObstaculo = pygame.image.load("bloqueObstaculo.png").convert_alpha()
    qbert = pygame.image.load("qbert.png").convert_alpha()
    enemigo1 = pygame.image.load("enemigo.png").convert_alpha()
    enemigo2 = pygame.image.load("enemigo2.png").convert_alpha()
    pantallaGanador = pygame.image.load("victoria.png").convert()
    pantallaPerdedor = pygame.image.load("derrota.png").convert()
    
    frames = 3
    animacionMuerte = []
    for i in range(frames):
        animacionMuerte.append(pygame.image.load("qbertMuere{}.png".format(i+1)).convert_alpha())
    
    pantallaInicio = pygame.image.load("inicio.jpg").convert()
    pantalla.blit(pantallaInicio, (0,0))
    
    fuente = pygame.font.SysFont('unispacebold', 64)
    
    pygame.display.flip()
    
    corriendo = True
    while corriendo:
        for event in pygame.event.get():
            
                if (event.type == pygame.QUIT):
                    corriendo = False
                
                #Controlar jugador1
                elif (event.type == pygame.KEYDOWN):
                    
                    if event.key == K_SPACE: #mueve hacia arriba
                        reiniciar = True
                        while reiniciar:
                            reiniciar, ganador, puntos = nivelPrincipal(pantalla, margen, dimensionMatrix, ancho, alto, clock, fondo, bloquePintado, bloqueDespintado, bloqueObstaculo, qbert, enemigo1, enemigo2, frames, animacionMuerte, fuente)
                        final(ganador, pantallaGanador, pantallaPerdedor, puntos, fuente)  
                            
                            
                    elif event.key == K_ESCAPE: #mueve hacia arriba
                        corriendo = False    
                        
                    elif event.key == K_i:
                        pantallaInstrucciones()
    sys.exit()


main()


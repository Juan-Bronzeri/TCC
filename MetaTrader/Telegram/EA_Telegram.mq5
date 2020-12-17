//+------------------------------------------------------------------+
//|                                                  EA_Telegram.mq5 |
//|                                                             Juan |
//+------------------------------------------------------------------+
#property copyright "Copyright 2020, CMTrade"
#property link      ""
#property version   "1.00"

#include <Telegram.mqh>

input string Token = ""; // Chave do bot

CCustomBot bot;

int respondeu;
#import "Comunicador.ex5"
   double profit();
#import


//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- create timer
   EventSetTimer(3);

   bot.Token(Token);
   if(bot.GetMe()!=0)
     {
      Print("Erro na inicialização do bot");
      return INIT_FAILED;
     }

//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();

  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---

  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
//---
   bot.GetUpdates(); // Obter mensagens
// Processar e enviar mensagens
   for(int i=0; i<bot.ChatsTotal(); i++)
     {
      respondeu = 0;

      CCustomChat *chat=bot.m_chats.GetNodeAtIndex(i);
      //--- se a mensagem não foi processada
      if(!chat.m_new_one.done)
        {
         chat.m_new_one.done=true;
         string text=chat.m_new_one.message_text;

         //--- início
         if(text=="/start")
           {
            respondeu = 1;
            bot.SendMessage(chat.m_id,"Olá! Bem-vindo!");
           }

         //--- ajuda
         if(text=="/update")
           {
            bot.SendMessage(chat.m_id,"A cotação do ativo " + _Symbol + " é: " + DoubleToString(SymbolInfoDouble(_Symbol, SYMBOL_ASK)+ "\xF4B0", 2));
            respondeu = 1;
            
           }
         if(text=="/volume")
         {
            bot.SendMessage(chat.m_id, "Mudando...");
            respondeu = 0.38;
         }
         if(text=="Ativos")
         {
             bot.SendMessage(chat.m_id, "");
         }
         if(respondeu == 0)
            bot.SendMessage(chat.m_id, "Fala direito comigo, eu não sou fluente ainda!");
        }
     }
  }
//+------------------------------------------------------------------+
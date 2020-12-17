//+------------------------------------------------------------------+
//|                                                  Comunicador.mq5 |
//|                                                             Juan |
//|                                                                  |
//+------------------------------------------------------------------+
#property copyright "Juan"
#property link      ""
#property version   "1.00"
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
double SL;
double Profit;

void OnStart()
  {
//---
   
  }
//+------------------------------------------------------------------+

float teste(float sl) export
{
    SL = sl;
    return SL;
}

double profit(double prof) export
{
if(prof == 1)
{
   return Profit;
}
   Profit = prof;
   return Profit;
}
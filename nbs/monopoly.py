import matplotlib.pyplot as plt
from sympy import diff, symbols, parse_expr, solve
import sympy
import math
import numpy as np
from free_market import *


class Monopoly(Free_market):
    def __init__(self, supply, demand) -> None:
        super().__init__(supply, demand)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
            
    def get_graph(self,complete = False) -> None:
        x = symbols('x')
        income = parse_expr(f"({self.demand}) * x")
        marginal_cost = self.supply
        marginal_revenue = diff(income, x)
        marginal_cost, marginal_revenue =str(marginal_cost), str(marginal_revenue)
        supply, demand =str(self.supply), str(self.demand)
        price = self.get_price()
        quantity = self.get_quantity()
        end = self.get_zero_point(self.demand)
        mc = self.get_calculate_values(marginal_cost, end)
        mr = self.get_calculate_values(marginal_revenue, end)
        mr_graph = {}
        for key in mr.keys():
            if mr[key] >= 0:
                mr_graph[key] = mr[key]
              

        supply_dict = self.get_calculate_values(supply, end)
        demand_dict = self.get_calculate_values(demand, end)

        if complete == True:
            x_range = [i for i in range(0, math.floor(quantity))] + [float(quantity)]
            if len(x_range) <= 1:
                x_range = [i for i in range(0, math.ceil(quantity))] + [float(quantity)]

            y_range = [i for i in range(0, math.floor(price))] + [float(price)]
            if len(y_range) <= 1:
                y_range = [i for i in range(0, math.ceil(price))] +[float(price)]


            price_curve = np.array([price for i in range(len(x_range))], dtype=float) 
            quantum_curve = np.array([quantity for i in range(len(y_range))], dtype=float) 

            plt.plot(x_range, price_curve, linestyle = "dashed", label = f"Price*: {round(price,2)}")
            
            plt.plot(quantum_curve,y_range, linestyle = "dashed", label = f"Quantity*: {round(quantity,2)}")
            
            #quantity_free_market = max(solve(Eq(parse_expr(self.supply), parse_expr(self.demand)), x))
            #equation_function = self.create_equation_function(self.demand)
            #if "x" not in self.supply:
            #    price_free_market = float(self.supply)
            #elif "x" not in self.demand:
            #    price_free_market = float(self.demand)
            #else:
            #   price_free_market = equation_function(quantity)

            mc_values = [mc[str(x)] if str(x) in mc else mc[round(x)] for x in x_range]  # Ensure mc values are aligned with x_range
            mc_array = np.array(mc_values, dtype=float)
            condition = mc_array  <= list(price_curve)
            producer_surplus_plot = plt.fill_between(x_range, mc_array, price_curve, where = condition, color = "silver", alpha=0.9) # producer surplus

            
            demand_array = np.array(list(demand_dict.values())[0:len(price_curve)], dtype=float)
            print(demand_array)
            condition = demand_array >= list(price_curve)
            consumer_surplus_plot = plt.fill_between(x_range, demand_array, price_curve, where = condition, color = "purple", alpha=0.9) # consumer surplus



            
        plt.plot(mc.keys(),mc.values(), label = "Marginal Cost") 
        plt.plot(mr_graph.keys(),mr_graph.values(), label = "Marginal Revenue") 

        
        plt.plot(demand_dict.keys(), demand_dict.values(), label = "Demand")

        plt.xlabel("Quantity")
        plt.ylabel("Price")

        plt.legend() 
        plt.show()

    def get_quantity(self) -> float:
        x = symbols('x')
        
        # Create the equation from the supply and demand functions
        mc = parse_expr(self.supply)
        revenue_eq = parse_expr(f"({self.demand})*(x)")
        mr = diff(revenue_eq, x)


        
        # Calculate the equilibrium price and quantity
        quantity = max(solve(Eq(mc, mr), x))
        #print(quantity)
        return quantity
    
    def get_price(self) -> float:
        x = symbols('x')
        quantity = self.get_quantity()
        mc = parse_expr(self.supply)
        revenue_eq = parse_expr(f"({self.demand})*(x)")
        mr = diff(revenue_eq, x)
        
    
        equation_function = self.create_equation_function(str(self.demand))
        
        
        if "x" not in str(mc):
            price = float(mc)
        elif "x" not in str(mr):
            price = float(mr)
        else:
            price = equation_function(quantity)
             
        #print(f"price is around {round(price, 3)}")
        return price


if __name__ == "__main__":
    total_cost = "x"
    demand = "10 - x"
    market = Monopoly(supply=total_cost, demand=demand)
    market.get_graph(complete=True, is_tot_cost=True)
    print(f"""{market.get_price()}{market.get_quantity()}{market.get_consumer_surplus()}{market.get_producer_surplus()}{market.get_economic_surplus()}""")
        














































""" class Monopoly(Free_Market):
    def __init__(self, supply, demand, revenue = 0, cost = 0,
                 marginal_revenue = 0, marginal_cost = 0, is_total_cost = False) -> None:
        
        self.is_total_cost = is_total_cost
        self.supply = supply
        self.demand = demand
        self.revenue = revenue
        self.cost = cost
        self.marginal_revenue = marginal_revenue
        self.marginal_cost = marginal_cost
        

        x = symbols('x')
        cost = self.supply

        demand_expr = parse_expr(self.demand)
        revenue = demand_expr * x
       
        if self.is_total_cost == True:
            cost_parsed = parse_expr(cost)
            marginal_cost = diff(cost_parsed, x)
        else:
            marginal_cost = cost

        
        marginal_revenue = diff(revenue, x)
        
        
        self.supply, self.demand =  self.supply, self.demand 
        self.revenue, self.cost = str(revenue), str(cost) 
        self.marginal_revenue, self.marginal_cost =  str(marginal_cost), str(marginal_revenue)
        



    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    

    def graph(self, complete = False) -> None:

        # Using instance variables supply and demand
        supply = self.supply
        demand = self.demand
        revenue = self.revenue
        cost = self.cost
        marginal_revnue = self.marginal_revenue
        marginal_cost = self.marginal_cost


        # We cannot take in a zero as either demand or supply, get the quantity and price
        print("cannot multiply variables with zero")
        price = self.get_price()
        quantity = self.get_quantity()
        

        # calculates the end variable, using for further calculations, may need to be improved
        start = 0
        if "x" in demand:
            end = self.get_zero_point(demand)
            end_floor = math.floor(end)

        else:
            end_floor = 2 * math.floor(quantity)
        step = 1 
        
        # Checks if we have a changing or constant supply
        if "x" in supply:
            supply_dict = self.get_calculate_values(supply, end) # end variable as final calculated value
            supply_curve = sorted(list(supply_dict.values()) + [float(price)])
            supply_curve_domain = sorted(list(supply_dict.keys()) + [float(quantity)]) 
            supply_dict[quantity] = price
            


            #supply_curve_plot = plt.plot(supply_dict.keys(), supply_dict.values(), label = "Supply") 
            plt.plot(supply_dict.keys(), supply_dict.values(), label = "Marginal Cost") 
            
        else:
            # If we constant supply then we know the price will be marginal cost and supply curve
            supply_list = [float(price) for i in range(start, math.ceil(end), step)] + [float(price)]
            supply_curve = supply_list

            
            #supply_curve_plot = plt.plot(supply_curve, label = "Supply") 
            plt.plot(supply_curve, label = "Marginal Cost") 
            
        # Checks if we have a changing or constant demand
        if "x" in demand:
            demand_dict = self.get_calculate_values(demand, end) # end variable as final calculated value
            demand_dict[quantity] =  price
            demand_curve = list(demand_dict.values()) + [float(price)] 
            demand_curve_domain = sorted(list(demand_dict.keys()) + [float(quantity)]) 

            #demand_curve_plot = plt.plot(demand_dict.keys(),demand_dict.values(), label = "Demand") 
            plt.plot(demand_dict.keys(),demand_dict.values(), label = "Demand") 
            
        else:
            demand_list = [float(price) for i in range(start, math.ceil(end), step)]
            demand_curve = demand_list + [float(price)]
            #demand_curve_plot = plt.plot(demand_curve, label = "Demand") 
            plt.plot(demand_curve, label = "Demand") 

        revenue_per_item = [elem/(i+1) for i, elem in enumerate(demand_curve)]
        plt.plot(revenue_per_item, label = "Revenue per item")


        # Checks if we have a changing or constant revenue
        if "x" in revenue:
            revenue_dict = self.get_calculate_values(revenue, end) # end variable as final calculated value
            #revenue_dict[quantity] =  price
            demand_curve = list(demand_dict.values())
            #demand_curve = [elem / (i+1) for i,elem in enumerate(demand_curve)]

            demand_curve_domain = sorted(list(revenue_dict.keys())) 

            #demand_curve_plot = plt.plot(demand_dict.keys(),demand_dict.values(), label = "Demand") 
            plt.plot(revenue_dict.keys(),revenue_dict.values(), label = "Revenue") 
            
        else:
            revenue_list = [float(price)/i  for i in range(start, math.ceil(end), step)]
            revenue_curve = revenue_list 
            #demand_curve_plot = plt.plot(demand_curve, label = "Demand") 
            plt.plot(revenue_curve, label = "Revenue") 
            

        plt.xlabel("Quantity")
        plt.ylabel("Price")
        
        if complete == True:
            
            x_range = [i for i in range(0, math.floor(quantity))] + [float(quantity)] 
            if len(x_range) <= 1:
                x_range = [i for i in range(0, math.ceil(quantity))] + [float(quantity)]

            y_range = [i for i in range(0, math.floor(price))] + [float(price)]
            if len(y_range) <= 1:
                y_range = [i for i in range(0, math.ceil(price))] +[float(price)]


            price_curve = np.array([price for i in range(len(x_range))], dtype=float) 
            quantum_curve = np.array([quantity for i in range(len(y_range))], dtype=float) 

            quantity_curve_plot = plt.plot(x_range,                              # x [i for i in range(len(price_curve))],
                                            price_curve,                         # y
                                            linestyle = "dashed", label = f"Price*: {price}")
            
            price_curve_plot = plt.plot(quantum_curve,                             # x 
                                        y_range,                                   # y [i for i in range(len(quantum_curve))]
                                        linestyle = "dashed", label = f"Quantity*: {quantity}") 
            
            plt.plot(x_range,                              # x [i for i in range(len(price_curve))],
                                            price_curve,                         # y
                                            linestyle = "dashed", label = f"Price*: {price}")
            
            plt.plot(quantum_curve,                             # x 
                                        y_range,                                   # y [i for i in range(len(quantum_curve))]
                                        linestyle = "dashed", label = f"Quantity*: {quantity}")
            
            

            if "x" in supply:
                price_curve = np.array(price_curve)
                supply_curve = np.array(supply_curve[0:len(price_curve) -1] + [float(price)])  
                
                x_range = np.array(x_range)
                
                # Create a valid boolean array for the 'where' condition
                condition = supply_curve[0:len(price_curve)]  <= price_curve

                demand_surplus_plot = plt.fill_between(x_range, supply_curve, price_curve, where = condition, color = "silver", alpha=0.9) # producer surplus

                x_width = float(quantity) * 0.4,
                y_height = (supply_curve[0] + price) * 0.6 if supply_curve[0] + price * 0.6 > price else price * 0.8


                plt.text(float(quantity) * 0.2, y_height * 0.8, "P.S")
                

            if "x" in demand:
                price_curve = np.array(price_curve)
                demand_curve = np.array(demand_curve[0:len(price_curve)  - 1] + [float(price)])  
                
                x_range = np.array(x_range)

                condition = demand_curve[0:len(price_curve)] >= price_curve
            
                consumer_surplus_plot = plt.fill_between(x_range, demand_curve, price_curve, where = condition, color = "purple", alpha=0.9) # consumer surplus

                y_height = (demand_curve[0] + price) * 0.4 if (demand_curve[0] + price) * 0.4 < price else price * 1.2
                plt.text(float(quantity) * 0.2, y_height * 1.2, "C.S")
            
            #print(f"x_range is: {x_range}\nsupply curve is:{supply_curve}\ndemand curve is: {demand_curve}\nprice curve is: {price_curve}")

        plt.legend(handles = [consumer_surplus_plot, 
                              demand_surplus_plot,
                              price_curve_plot,
                              quantity_curve_plot,
                              demand_curve_plot,
                              supply_curve_plot], 
                              labels = ("Consumer Surplus", "Producer Surplus","Price*","Quantity*", 
                                        "Demand", "Supply")) 
        plt.legend()
        plt.show()
    

if __name__ == "__main__":
    total_cost = "100 + 2*x**2 "
    demand = "10 - 2*x"
    market = Monopoly(supply=total_cost, demand=demand, is_total_cost= True)
    market.graph(complete=True)
    market.get_price()
         """




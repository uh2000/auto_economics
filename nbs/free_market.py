import matplotlib.pyplot as plt
from sympy import solve, Eq, symbols, parse_expr
import sympy
import numpy as np
import random
import math

class Free_market:
    def __init__(self, supply, demand) -> None:
        self.supply = supply
        self.demand = demand
        
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def get_graph(self, complete: bool = False) -> None:
        print("cannot multiply variables with zero")
        price = self.get_price()
        quantity = self.get_quantity()
        
        start = 0
        if "x" in self.demand:
            end = math.floor(self.get_zero_point(self.demand))
        else:
            end = 1.5 * math.floor(quantity)
        step = 1 
        

        if "x" in self.supply:
            supply_dict = self.get_calculate_values(self.supply, end)
            supply_curve = sorted(list(supply_dict.values()) + [float(price)])
            #supply_curve_domain = sorted(list(supply_dict.keys()) + [float(quantity)]) 
            supply_dict[quantity] = price


            #supply_curve_plot = plt.plot(supply_dict.keys(), supply_dict.values(), label = "Supply") 
            plt.plot(supply_dict.keys(), supply_dict.values(), label = "Supply") 
            
        else:
            supply_list = [float(price) for i in range(start, math.ceil(end), step)] + [float(price)]
            supply_curve = supply_list

            
            #supply_curve_plot = plt.plot(supply_curve, label = "Supply") 
            plt.plot(supply_curve, label = "Supply") 
            
        
        if "x" in self.demand:
            demand_dict = self.get_calculate_values(self.demand, end)
            demand_dict[quantity] =  price
            demand_curve = list(demand_dict.values()) + [float(price)]
            #demand_curve_domain = sorted(list(demand_dict.keys()) + [float(quantity)]) 

            #demand_curve_plot = plt.plot(demand_dict.keys(),demand_dict.values(), label = "Demand") 
            plt.plot(demand_dict.keys(),demand_dict.values(), label = "Demand") 
            
        else:
            demand_list = [float(price) for i in range(start, math.ceil(end), step)]
            demand_curve = demand_list + [float(price)]
            #demand_curve_plot = plt.plot(demand_curve, label = "Demand") 
            plt.plot(demand_curve, label = "Demand") 
            

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
            
            plt.plot(x_range,                              # x [i for i in range(len(price_curve))],
                                            price_curve,                         # y
                                            linestyle = "dashed", label = f"Price*: {price}")
            
            plt.plot(quantum_curve,                             # x 
                                        y_range,                                   # y [i for i in range(len(quantum_curve))]
                                        linestyle = "dashed", label = f"Quantity*: {quantity}")
            
            

            if "x" in self.supply:
                price_curve = np.array(price_curve)
                supply_curve = np.array(supply_curve[0:len(price_curve) -1] + [float(price)])  

                x_range = np.array(x_range)

                # Create a valid boolean array for the 'where' condition
                condition = supply_curve[0:len(price_curve)]  <= price_curve

                demand_surplus_plot = plt.fill_between(x_range, supply_curve, price_curve, where = condition, color = "silver", alpha=0.9) # producer surplus

                x_mid = np.quantile(x_range, 0.2)
                y_mid = np.quantile([np.min(supply_curve[condition]), np.max(price_curve[condition])], 0.8)

                plt.text(x_mid, y_mid, "P.S")

            if "x" in self.demand:
                price_curve = np.array(price_curve)
                demand_curve = np.array(demand_curve[0:len(price_curve)  - 1] + [float(price)])  

                x_range = np.array(x_range)

                condition = demand_curve[0:len(price_curve)] >= price_curve

                consumer_surplus_plot = plt.fill_between(x_range, demand_curve, price_curve, where = condition, color = "purple", alpha=0.9) # consumer surplus

                x_mid = np.quantile(x_range, 0.2)
                y_mid = np.quantile([np.min(price_curve[condition]), np.max(demand_curve[condition])], 0.2)

                plt.text(x_mid, y_mid, "C.S")

        

        plt.legend()
        plt.show()


    def get_calculate_values(self, expression: str, end: int) -> dict:
        start = 0
        step = 1 

        quantity = end
        end = math.ceil(end)

        value_pairs = {}
        equation_function = self.create_equation_function(expression)

        
        if equation_function:
            #value_pairs[x_val] = result """
            if end <= 1:
                x_values = sorted([i for i in range(start, end, step)] + [quantity])

                for x_val in x_values:
                    result = float(equation_function(x_val))
                    value_pairs[x_val] = result
                result = float(equation_function(quantity))

                value_pairs[x_val] = result


            else:
                x_values = sorted([i for i in range(start, end, step)] + [quantity])
                for x_val in x_values:
                    result = float(equation_function(x_val))
                    value_pairs[x_val] = result
                
                
               # print(f"For x = {x_val}, the result is {result}")

        else:
            print("Error: Unable to create the equation function.")
        return value_pairs    
    

    def create_equation_function(self, equation_str: str) -> str:
        x = symbols('x')
        
        try:
            equation = parse_expr(equation_str)
            equation_function = lambda x_val: equation.subs(x, x_val)
            return equation_function
        except Exception as e:
            return None


    def get_zero_point(self, expression: str) -> float:
        x = symbols('x')
        
        # Create the equation from the supply and demand functions
        equation = parse_expr(expression)
        
        # Calculate the equilibrium price and quantity
        solutions = solve(equation, x)
        if solutions:
            zero_point = solutions[0]
            #print(f"zero_points {zero_point}")
            return zero_point
        else:
            zero_point = self.get_price(self.supply, self.demand)
            return zero_point + round(0.1*zero_point, 0)
    
    
    def get_quantity(self) -> float:
        x = symbols('x')
        
        # Create the equation from the supply and demand functions
        supply_eq = parse_expr(self.supply)
        demand_eq = parse_expr(self.demand)
        
        # Calculate the equilibrium price and quantity
        quantity = max(solve(Eq(supply_eq, demand_eq), x))
        #print(quantity)
        return quantity
    

    def get_price(self) -> float:
        x = symbols('x')
        quantity = self.get_quantity()
        
        if "x" in self.demand:
            end = self.get_zero_point(self.demand)
        else:
            end = 2 * quantity
        
        equation_function = self.create_equation_function(self.demand)
        
        
        if "x" not in self.supply:
            price = float(self.supply)
        elif "x" not in self.demand:
            price = float(self.demand)
        else:
            price = equation_function(quantity)
             
        #print(f"price is around {round(price, 3)}")
        return price


    def get_consumer_surplus(self) -> float:
        x, y = symbols('x y')
        
        
        # Calculate the equilibrium price and quantity
        price = self.get_price()
        quantity = self.get_quantity()
        
        # Define the inverse demand function (price as a function of quantity)
        consumer_surplus = parse_expr(f"{self.demand}-{price}")
        
        # Calculate consumer surplus
        surplus = sympy.integrate(consumer_surplus, (x, 0, quantity)) 
        
        return surplus
    

    def get_producer_surplus(self) -> float:
        x, y = symbols('x y')
        
        # Create the equation from the supply and demand functions
        supply_eq = parse_expr(self.supply)
        demand_eq = parse_expr(self.demand)
        
        # Calculate the equilibrium price and quantity
        price = self.get_price()
        quantity = self.get_quantity()
                
        
        #producer_surplus = parse_expr(f"{price}-{self.supply}")
        price_line = sympy.integrate(parse_expr(f"{price}"), (x, 0, quantity))
        supply_curve = sympy.integrate(parse_expr(self.supply), (x, 0, quantity))

        
            
        
        # Calculate consumer surplus
        surplus = price_line - supply_curve
        
        return surplus


    def get_economic_surplus(self) -> float:
        consumer = self.get_consumer_surplus()
        producer = self.get_producer_surplus()
        economic_surplus = consumer + producer
        return economic_surplus
    



    
if __name__ == "__main__":
    
        for i in range(0, 5):
            a = random.randint(1,5)
            b = random.randint(5,10)
            c = random.randint(1,5)
            d = random.randint(0,1)

            supply_function = f"{d} + {c} * x"
            demand_function = f"{b} - {a} * x"
            market = Free_market(supply_function, demand_function)
            

            print(f"supply function {supply_function}\ndemand function {demand_function}")
            market.get_graph(complete=True)
        


bad_cases = ["supply function 0 + 1 * x demand function 9 - 5 * x",
             "supply function 1 + 1 * x demand function 10 - 2 * x"]
def calcular(*args):
    personas = {}
    for p in args:
        for persona, monto in p:
            if persona in personas:
                personas[persona].append(("Total", monto))
            else:
                personas[persona] = [("Total", monto)]

    
    def split_expenses(expenses):
    
        # Step 1: Calculate each person's total expenses
        totals = {}
        for payer, expenses_list in expenses.items():
            for expense in expenses_list:
                _, amount = expense
                if payer not in totals:
                    totals[payer] = amount
                else:
                    totals[payer] += amount

        # Step 2: Calculate the group's total expenses and the average expense per person
        group_total = sum(totals.values())
        num_people = len(expenses)
        avg_expense = group_total / num_people
        todos_deben = avg_expense            


        # Step 3: Calculate how much each person owes or is owed
        debts = {}
        for payer, total_paid in totals.items():
            amount_owed = total_paid - avg_expense
            if amount_owed > 0:
                # This person is owed money
                for payee, payee_total in totals.items():
                    if payee_total - avg_expense < 0:
                        # This person owes money and can pay some of what they owe
                        amount_to_pay = min(amount_owed, avg_expense - payee_total)
                        if payer not in debts:
                            debts[payer] = {payee: round(amount_to_pay)}
                        else:
                            debts[payer][payee] = round(amount_to_pay)
                        amount_owed -= amount_to_pay
                        if amount_owed == 0:
                            break
            elif amount_owed < 0:
                # This person owes money
                for payee, payee_total in totals.items():
                    if payee_total - avg_expense > 0:
                        # This person is owed money and can be paid some of what they are owed
                        amount_to_receive = min(-amount_owed, payee_total - avg_expense)
                        if payer not in debts:
                            debts[payer] = {payee: round(-amount_to_receive)}
                        else:
                            debts[payer][payee] = round(-amount_to_receive)
                        amount_owed += amount_to_receive
                        if amount_owed == 0:
                            break
        return debts, todos_deben
  
    cuentas, todos_deben = split_expenses(personas)

    amistades_claras = [f"Todos deben: {round(todos_deben)}"]
    for c in cuentas:
        for d in cuentas[c]:
            if cuentas[c][d] < 0:
                deuda = str(cuentas[c][d])
                amistades_claras.append(f"{c} le debe {deuda[1:]} a {d}")

    return amistades_claras





from tools.ohio_statute_tool import OhioStatuteTool


tool = OhioStatuteTool()


test_queries = [
    """
    Seller and Buyer verbally agreed to the sale
    of office furniture for $1,200. No written
    agreement was signed.
    """,

    """
    The parties verbally agreed to modify the
    existing contract and increase the quantity
    of equipment.
    """,

    """
    Seller failed to deliver the generators by
    the delivery deadline and informed Buyer that
    it would not perform.
    """,

    """
    Buyer accepted all goods but failed to make
    payment when payment became due.
    """
]


for index, query in enumerate(
    test_queries,
    start=1
):

    print("\n" + "=" * 70)

    print(
        f"RETRIEVAL TEST {index}"
    )

    print("=" * 70)

    result = tool.search_statutes(query)

    print(result)
class NewTaipeiCityService:

    def __init__(self, session_factory, repository_cls):
        self._session_factory = session_factory
        self._repository_cls = repository_cls

    def create_pre_sale_house_transactions(self, transactions):
        with self._session_factory() as session:
            repo = self._repository_cls(session)
            repo.bulk_insert(transactions)

            session.commit()

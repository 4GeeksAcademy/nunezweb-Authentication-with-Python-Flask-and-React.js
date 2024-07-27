import React, { useContext } from "react";
import { Context } from "../store/appContext";
import "../../styles/private.css";

export const Private = () => {
  const { store } = useContext(Context);

  return (
    <div className="private-area p-5">
      {store.token == null ? (
        <div className="card p-5">
          <div className="card-body">
            <h2 className="card-title">You do not have access to this section</h2>
            <p className="card-text mt-3">
              You must log in as a registered user to view the content of this page.
            </p>
          </div>
        </div>
      ) : (
        <div className="card p-5">
          <div className="card-body">
            <h2 className="card-title">Welcome to the Private Area</h2>
            <p className="card-text mt-3">
              Enjoy exclusive access to our private resources and personalized content. Feel free to explore and make the most of the tools available to you.
            </p>
          </div>
          <img src="https://picsum.photos/600/200" alt="Welcome Image" />
        </div>
      )}
    </div>
  );
};
